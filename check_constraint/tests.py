import os

from django.test import TestCase

DATABASES = ['default']


if 'ENV_DB' in os.environ:
    DATABASES += [os.environ['ENV_DB']]

class AnnotateCheckConstraintTestCase(TestCase):
    databases = DATABASES
    def test_dummy_setup(self):
        self.assertEqual(1, 1)
