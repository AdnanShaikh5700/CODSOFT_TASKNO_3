from django.db import models
from django.utils import timezone

from datetime import date
from django.conf import settings

# Create your models here.

class IssuedBook(models.Model):
  book = models.ForeignKey('books.Book', on_delete=models.PROTECT, related_name='issue_history')
  member = models.ForeignKey('members.Member', on_delete=models.PROTECT, related_name='borrow_history')
  issue_date = models.DateField(default=timezone.localdate)
  due_date = models.DateField()
  return_date = models.DateField(null=True, blank=True)

  def __str__(self):
    return f"{self.book.title} - {self.member.name}"

  @property
  def is_returned(self):
    return self.return_date is not None

  @property
  def overdue_days(self):
    end_date = self.return_date or timezone.localdate()
    return max(0, (end_date - self.due_date).days)

  @property
  def late_fee(self):
    daliy_fee = settings.LIBRARY_DALIY_LATE_FEE
    return self.overdue_days * daliy_fee