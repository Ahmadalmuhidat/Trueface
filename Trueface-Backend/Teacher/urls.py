from django.urls import path
from .controllers import lectures, students, attendance, health

urlpatterns = [
  # health
  path('', health.health),

  # attendance
  path('attendance/insert', attendance.InsertAttendance),
  path('attendance/delete', attendance.DeleteAttendance),
  path('attendance/clear_class', attendance.ClearClassAttendance),

  # lectures
  path('lectures/get_by_teacher', lectures.GetLecturesByTeacher),
  path('lectures/delete', lectures.DeleteLecture),
  path('lectures/clear_data', lectures.ClearLectureData),

  # students
  path('students/get_by_lecture', students.GetStudentsByLecture),
  path('students/remove_from_class', students.RemoveStudentFromClass),
  path('students/clear_attendance', students.ClearStudentAttendance)
]
