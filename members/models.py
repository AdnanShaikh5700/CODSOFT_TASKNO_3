from django.db import models

# Create your models here.

class Member(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=10, blank=True)
  address = models.TextField(blank=True)
  joined_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name