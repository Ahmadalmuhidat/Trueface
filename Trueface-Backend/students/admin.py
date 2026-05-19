from django.contrib import admin

from students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ["id", "first_name", "middle_name", "last_name", "gender"]
  list_filter = ["gender"]
  search_fields = ["id", "first_name", "middle_name", "last_name"]
  ordering = ["id"]
