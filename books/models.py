from django.db import models

# Create your models here.


class Author(models.Model):
  name = models.CharField(max_length=100)
  biography = models.TextField(blank=True)

  def __str__(self):
    return self.name


class Book(models.Model):
  title = models.CharField(max_length=150)
  isbn = models.CharField(max_length=13, unique=True)
  author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
  category = models.CharField(max_length=100, blank=True)
  total_copies = models.PositiveIntegerField(default=1)
  available_copies = models.PositiveIntegerField(default=1)

  def __str__(self):
    return self.title
  