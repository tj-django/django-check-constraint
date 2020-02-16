from django.db import models

from django.db.models.sql import Query


class AnnotatedCheckConstraint(models.CheckConstraint):
    def __init__(self, *args, annotations=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.annotations = annotations or {}

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
        kwargs["check"] = self.check
        kwargs["annotations"] = self.annotations

        return path, args, kwargs
