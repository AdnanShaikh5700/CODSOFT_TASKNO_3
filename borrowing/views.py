from django.shortcuts import render
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from books.models import Book
from members.models import Member
from .models import IssuedBook
from .serializer import IssuedBookSerializer

# Create your views here.


class IssuedBookViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = IssuedBook.objects.select_related("book", "member").all().order_by("-issue_date", "-id")
  serializer_class = IssuedBookSerializer

  @action(detail=False, methods=["post"])
  def issue(self, req):
    book_id = req.data.get("book")
    member_id = req.data.get("member")
    due_date = req.data.get("due_date")

    if not book_id or not member_id or not due_date:
      raise
    ValidationError("Book, Member Or Due_Date Are Required..")

    try:
        due_date = timezone.datetime.strptime(due_date, "%Y-%m-%d").date()
    except(ValueError, TypeError):
       raise 
    ValidationError("Due_Date Must Use YYYY-MM-DD Formate..")

    if due_date < timezone.localdate():
       raise ValidationError("Due Date Cannot Be In The Past")

    with transaction.atomic():
       book = get_object_or_404(Book.objects.select_for_update(), pk=book_id)
       member = get_object_or_404(Member, pk=member_id)

       if IssuedBook.objects.filter(book=book, member=member, return_date__isnull=True).exists():
          raise ValidationError("This Member Already Has This Book Issued..")
       updated = Book.objects.filter(pk=book.pk,available_copies__gt=0).update(available_copies=F("available_copies") - 1)

       if updated == 0:
          raise ValidationError("No Copies Of This Book Are Available..")
       issue = IssuedBook.objects.create(book=book, member=member, due_date=due_date)
       return Response(IssuedBookSerializer(issue).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def return_book(self, req, pk=None):
       with transaction.atomic():
          issue = get_object_or_404(IssuedBook.objects.select_for_update(), pk=pk)
          if issue.return_date is not None:
             raise 
          ValidationError("This Book Has Already Been Returned..")
          Book.objects.filter(pk=issue.book_id).update(available_copies=F("available_copies") + 1)
          issue.return_date = timezone.localdate()
          issue.save(update_fields=["return_date"])
          return Response(
             IssuedBookSerializer(issue).data,status=status.HTTP_200_OK
          )

    @action(detail=False, methods=["get"])
    def overdue(self, req):
       today = timezone.localdate()

       issues = self.get_queryset().filter(
          return_date__isnull=True,
          due_date__lt=today
       )   

       page = self.paginate_queryset(issues)

       if page is not None:
          serializer = self.get_serializer(page, many=True)
          return self.get_paginated_response(serializer.data)
       serializer = self.get_serializer(issues, many=True)
       return Response(serializer.data)


      # serializer = self.get_serializer(issues, many=True)
      #       return Response(serializer.data)     