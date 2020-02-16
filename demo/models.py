from django.contrib.auth import get_user_model
from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Books, through="LibraryBooks")


class LibraryBooks(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="library_books"
    )
    books = models.ForeignKey(Books, on_delete=models.PROTECT)
