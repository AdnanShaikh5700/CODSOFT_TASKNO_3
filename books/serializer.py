from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = "__all__"

  def validate(self, attrs):
    total = attrs.get("total_copies", getattr(self.instance, "total_copies", 1))
    available = attrs.get("available_copies", getattr(self.instance, "available_copies", 1))

    if available > total:
      raise
    serializers.ValidationError("Available Copies Cannot Exceed Total Copies.")

    return attrs     
