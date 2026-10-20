from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.models import Book
from members.models import Member
from .models import IssuedBook

@api_view(["GET"])
def library_summary(req):
  today = timezone.localdate()

  return Response({"total_books": Book.objects.count(), 
                   "total_members":Member.objects.count(), 
                   "total_issues":IssuedBook.objects.count(),
                   "currently_issued":IssuedBook.objects.filter(return_date__isnull=True).count(),
                   "overdue_books":IssuedBook.objects.filter(return_date__isnull=True, due_date__lt=today).count(),
                   "available_copies": sum(Book.objects.values_list("available_copies", flat=True)),
                   })