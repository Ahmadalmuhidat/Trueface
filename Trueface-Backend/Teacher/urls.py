from django.urls import path
from .controllers import classes, students, attendance, health

urlpatterns = [
  # health
  path('', health.health),

  # attendance
  path('get_attendance_by_class', attendance.GetAttendanceByClass),
  path('search_attendance', attendance.SearchAttendance),
  path('check_attendance', attendance.CheckAttendance),
  path('insert_attendance', attendance.InsertAttendance),

  # classes
  path('get_classes_by_teacher', classes.GetClassesByTeacher),

  # studnets
  path('get_students_by_class', students.GetStudentsByClass)
]
