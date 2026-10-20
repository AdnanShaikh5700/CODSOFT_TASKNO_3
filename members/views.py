from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .models import Member
from .serializer import MemberSerializer

# Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
  queryset = Member.objects.all().order_by("id")
  serializer_class = MemberSerializer

  filter_backends = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter
  ]

  search_fields = ["name", "email", "phone"]
  ordering_fields = ["name", "joined_at", "id"]
