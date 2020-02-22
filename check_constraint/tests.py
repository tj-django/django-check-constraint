from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, DatabaseError
from django.test import TestCase

from demo.models import Book

# TODO: Fix sqlite
User = get_user_model()


class AnnotateCheckConstraintTestCase(TestCase):
    databases = settings.TEST_ENV_DB

    @classmethod
    def setUpTestData(cls):
        for db_name in cls._databases_names(include_mirrors=False):
            cls.user = User.objects.db_manager(db_name).create_superuser(
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

    def test_create_is_invalid_with_annotated_check_constraint(self):
        for db_name in self._databases_names(include_mirrors=False):
            if db_name == "mysql":
                with self.assertRaises(DatabaseError):
                    Book.objects.using(db_name).create(
                        name="Business of the 21st Century",
                        created_by=self.user,
                        amount=Decimal("50"),
                    )
            else:
                with self.assertRaises(IntegrityError):
                    Book.objects.using(db_name).create(
                        name="Business of the 21st Century",
                        created_by=self.user,
                        amount=Decimal("50"),
                    )
