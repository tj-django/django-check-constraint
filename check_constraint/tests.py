import os
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import DEFAULT_DB_ALIAS

from django.test import TestCase

from demo.models import Book

User = get_user_model()

# TODO: Fix sqlite3.
DATABASES = set()


if "ENV_DB" in os.environ:
    DATABASES.add(os.environ["ENV_DB"])


class AnnotateCheckConstraintTestCase(TestCase):
    databases = DATABASES

    @classmethod
    def setUpTestData(cls):
        for db_name in cls._databases_names(include_mirrors=False):
            cls.user = User.objects.using(db_name).create_superuser(
                username="Admin", email="admin@admin.com", password="test",
            )

    def test_create_passes_with_annotated_check_constraint(self):
        for db_name in self._databases_names(include_mirrors=False):
            book = Book.objects.using(db_name).create(
                name="Business of the 21st Century",
                created_by=self.user,
                amount=Decimal("50"),
                amount_off=Decimal("20.58"),
            )

            self.assertEqual(book.name, "Business of the 21st Century")
            self.assertEqual(book.created_by, self.user)
