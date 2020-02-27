from decimal import Decimal
from unittest.mock import patch, PropertyMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, DatabaseError, connections
from django.test import TestCase, TransactionTestCase

from demo.models import Book

# TODO: Fix sqlite

User = get_user_model()


class AnnotatedCheckConstraintNameTestCase(TransactionTestCase):
    databases = settings.TEST_ENV_DB

    @patch("django.VERSION", new_callable=PropertyMock(return_value=(2, 2)))
    def test_correct_name_is_generated_for_django_less_than_30(self, version):
        for db_alias in self._databases_names(include_mirrors=False):
            connection = connections[db_alias]

            connection.disable_constraint_checking()

            for constraint in Book._meta.constraints:
                name = "%(app_label)s_%(class)s_optional_field_provided"
                constraint.model = "demo.Book"
                constraint.name = name

                path, args, kwargs = constraint.deconstruct()

                self.assertEqual(kwargs["name"], "demo_book_optional_field_provided")


class AnnotatedCheckConstraintTestCase(TestCase):
    databases = settings.TEST_ENV_DB

    @classmethod
    def setUpTestData(cls):
        for db_alias in cls._databases_names(include_mirrors=False):
            cls.user = User.objects.db_manager(db_alias).create_superuser(
                username="Admin", email="admin@admin.com", password="test",
            )

    def test_create_passes_with_annotated_check_constraint(self):
        for db_alias in self._databases_names(include_mirrors=False):
            book = Book.objects.using(db_alias).create(
                name="Business of the 21st Century",
                created_by=self.user,
                amount=Decimal("50"),
                amount_off=Decimal("20.58"),
            )

            self.assertEqual(book.name, "Business of the 21st Century")
            self.assertEqual(book.created_by, self.user)

    def test_create_is_invalid_with_annotated_check_constraint(self):
        for db_alias in self._databases_names(include_mirrors=False):
            if db_alias == "mysql":
                with self.assertRaises(DatabaseError):
                    Book.objects.using(db_alias).create(
                        name="Business of the 21st Century",
                        created_by=self.user,
                        amount=Decimal("50"),
                    )
            else:
                with self.assertRaises(IntegrityError):
                    Book.objects.using(db_alias).create(
                        name="Business of the 21st Century",
                        created_by=self.user,
                        amount=Decimal("50"),
                    )
