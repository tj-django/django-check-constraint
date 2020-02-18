from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from check_constraint.models import AnnotatedCheckConstraint
from demo.models.function import NotNullCount


class Book(models.Model):
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=9, decimal_places=2,)
    amount_off = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
    )
    percentage = models.DecimalField(
        max_digits=3, decimal_places=0, null=True, blank=True,
    )

    class Meta:
        constraints = [
            AnnotatedCheckConstraint(
                check=Q(not_null_count=1),
                annotations={
                    "not_null_count": (NotNullCount("amount_off", "percentage",)),
                },
                name="%(app_label)s_%(class)s_optional_field_provided",
            ),
        ]
