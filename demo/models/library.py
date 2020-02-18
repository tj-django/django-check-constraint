from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField("Book", through="LibraryBook")


class LibraryBook(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="library_books"
    )
    books = models.ForeignKey("Book", on_delete=models.PROTECT)
