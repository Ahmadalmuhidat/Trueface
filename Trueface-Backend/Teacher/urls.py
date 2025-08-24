from django.urls import path
from .controllers import lectures, students, attendance, health

urlpatterns = [
  # health
  path('', health.health),

  # attendance
  path('attendance/insert', attendance.InsertAttendance),

  # lectures
  path('lectures/get_by_teacher', lectures.GetLecturesByTeacher),

  # studnets
  path('studnets/get_by_lecture', students.GetStudentsByLecture)
]
