# django-check-constraint
![django check constraint test.](https://github.com/jackton1/django-check-constraint/workflows/django%20check%20constraint%20test./badge.svg?branch=master)
[![PyPI - License](https://img.shields.io/pypi/l/django-check-constraint.svg)](https://github.com/jackton1/django-check-constraint/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-check-constraint.svg)](https://pypi.org/project/django-check-constraint)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-check-constraint.svg)](https://docs.djangoproject.com/en/2.2/releases/)

Complex check constraint support for Django.


#### Scenario:

Suppose you have a database function that returns the counts of null values in `[i, ...n]`.

```postgresql
CREATE OR REPLACE FUNCTION public.non_null_count(VARIADIC arg_array ANYARRAY)
  RETURNS BIGINT AS
  $$
    SELECT COUNT(x) FROM UNNEST($1) AS x
  $$ LANGUAGE SQL IMMUTABLE;

```

#### Example:
```postgresql
SELECT public.non_null_count(1, null, null);
```

#### Outputs:

```sql
non_null_count
----------------
              1
(1 row)
```

Defining a check constraint with this function

The equivalent of

```postgresql
ALTER TABLE app_name_test_modoel ADD CONSTRAINT app_name_test_model_optional_field_provided
    CHECK(non_null_count(amount::integer , amount_off::integer, percentage::integer) = 1);
```

## Usage

Converting this to django functions and annotated check contraints can be done using:

`function.py`

```python
from django.db.models import Func, SmallIntegerField, TextField
from django.db.models.functions import Cast


class NotNullCount(Func):
    function = 'non_null_count'

    def __init__(self, *expressions, **extra):
        filter_exp = [
            Cast(exp, TextField()) for exp in expressions if isinstance(exp, str)
        ]
        if 'output_field' not in extra:
            extra['output_field'] = SmallIntegerField()

        if len(expressions) < 2:
            raise ValueError('NotNullCount must take at least two expressions')

        super().__init__(*filter_exp, **extra)
```



#### Creating annotated check constraints


```python
from django.db import models
from django.db.models import Q
from check_constraint.models import AnnotatedCheckConstraint

class TestModel(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    amount_off = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)


    class Meta:
        constraints = [
            AnnotatedCheckConstraint(
                check=Q(not_null_count=1),
                annotations={
                    'not_null_count': (
                        NotNullCount(
                            'amount',
                            'amount_off',
                            'percentage',
                        )
                    ),
                },
                name='%(app_label)s_%(class)s_optional_field_provided',
            ),
        ]

```


TODO's
------

- [ ] Add support for schema based functions.
