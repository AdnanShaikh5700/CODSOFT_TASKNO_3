from rest_framework import serializers
from .models import IssuedBook

class IssuedBookSerializer(serializers.ModelSerializer):
  
  overdue_days = serializers.ReadOnlyField()
  late_fee = serializers.ReadOnlyField()

  class Meta:
    model = IssuedBook
    fields = "__all__"
    read_only_fields = ["issue_date , return_date", "overdue_days", "late_fee"]