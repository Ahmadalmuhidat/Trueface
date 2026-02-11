from django.urls import path
from .controllers import lectures, students, attendance, health

urlpatterns = [
  # health
  path('', health.health),

  # attendance
  path('attendance/insert', attendance.InsertAttendance),
  path('attendance/delete', attendance.DeleteAttendance),
  path('attendance/clear_lecture', attendance.ClearLectureAttendance),

  # lectures
  path('lectures/get_by_teacher', lectures.GetLecturesByTeacher),
  path('lectures/delete', lectures.DeleteLecture),
  path('lectures/clear_data', lectures.ClearLectureData),

  # students
  path('students/get_by_lecture', students.GetStudentsByLecture),
  path('students/remove_from_lecture', students.RemoveStudentFromLecture),
  path('students/clear_attendance', students.ClearStudentAttendance)
]
