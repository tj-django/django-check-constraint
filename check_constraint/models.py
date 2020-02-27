import django
from django.apps import apps
from django.db import models

from django.db.models.sql import Query

__all__ = ["AnnotatedCheckConstraint"]


class AnnotatedCheckConstraint(models.CheckConstraint):
    def __init__(self, *args, model=None, annotations=None, **kwargs):
        self._model = model
        self.annotations = annotations or {}
        super(AnnotatedCheckConstraint, self).__init__(*args, **kwargs)

    @property
    def model(self):
        if self._model:
            return apps.get_model(self._model)
        return self._model

    @model.setter
    def model(self, new_model):
        self._model = new_model

    def _get_check_sql(self, model, schema_editor):
        query = Query(model=model)

        # Add annotations
        for k, v in self.annotations.items():
            query.add_annotation(v, k)

        where = query.build_where(self.check)

        compiler = query.get_compiler(connection=schema_editor.connection)

        sql, params = where.as_sql(compiler, schema_editor.connection)

        return sql % tuple(schema_editor.quote_value(p) for p in params)

    def deconstruct(self):
        path, args, kwargs = super(models.CheckConstraint, self).deconstruct()

        if (2, 0) <= django.VERSION <= (3, 0) and self.model:
            # noinspection PyProtectedMember
            kwargs["name"] = kwargs["name"] % {
                "app_label": self.model._meta.app_label.lower(),
                "class": self.model.__name__.lower(),
            }

        kwargs["check"] = self.check
        kwargs["annotations"] = self.annotations

        return path, args, kwargs
