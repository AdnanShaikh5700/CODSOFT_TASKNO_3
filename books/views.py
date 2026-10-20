from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Author, Book
from .serializer import BookSerializer, AuthorSerializer

# Create your views here.

class AuthorViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all().order_by("id")
  serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
  queryset = Book.objects.select_related("author").all().order_by("id")
  serializer_class = BookSerializer

  filter_backends = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter
  ]

  filterset_fields = ["author", "category"]
  search_fields = ["title", "isbn", "author"]  
  ordering_fields = ["title", "id", "total_copies"]
