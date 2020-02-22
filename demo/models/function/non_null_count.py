from django.db.models import Func, SmallIntegerField, TextField
from django.db.models.functions import Cast


class NotNullCount(Func):
    function = "non_null_count"

    def __init__(self, *expressions, **extra):
        filter_exp = [
            Cast(exp, TextField()) for exp in expressions if isinstance(exp, str)
        ]
        if "output_field" not in extra:
            extra["output_field"] = SmallIntegerField()

        if len(expressions) < 2:
            raise ValueError("NotNullCount must take at least two expressions")

        super().__init__(*filter_exp, **extra)

    def as_sqlite(self, compiler, connection, **extra_context):
        connection.ops.check_expression_support(self)
        sql_parts = []
        params = []
        for arg in self.source_expressions:
            arg_sql, arg_params = compiler.compile(arg)
            sql_parts.append(arg_sql)
            params.extend(arg_params)
        data = {**self.extra, **extra_context}
        data["template"] = "%(function)s(%(expressions)s)"
        arg_joiner = self.arg_joiner
        data["function"] = self.function
        data["expressions"] = data["field"] = arg_joiner.join(sql_parts)
        template = data["template"]

        return template % data, params
