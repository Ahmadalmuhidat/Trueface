from django.contrib import admin

from attendance.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
  list_display = ["id", "student", "lecture_field", "date", "time"]
  list_filter = ["date", "lecture_field"]
  search_fields = ["student__first_name", "student__last_name", "student__id", "lecture_field__id"]
  ordering = ["-date", "-time"]
