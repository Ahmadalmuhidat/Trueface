from django.urls import path
from .controllers import lectures, users, students, courses

urlpatterns = [
  # users
  path('users/get_all', users.GetUsers),
  path('users/insert', users.InsertUser),
  path('users/remove', users.RemoveUser),
  path('login', users.login),

  # students
  path('students/insert', students.InsertStudent),
  path('students/remove', students.RemoveStudent),
  path('students/get_all', students.GetAllStudents),

  # lectures
  path('lectures/get_all', lectures.GetLectures),
  path('lectures/remove', lectures.RemoveLecture),
  path('lectures/insert', lectures.InsertLecture),
  path('lectures/add_student', lectures.AddStudentToLecture),
  path('lectures/clear', lectures.ClearLecture),
  path('lectures/get_students', lectures.GetStudentLectures), # remove
  path('lectures/remove_student', lectures.RemoveStudentFromLecture),

  # courses
  path("courses/get_all", courses.GetCourses),
  path("courses/remove", courses.RemoveCourse),
  path("courses/insert", courses.InsertCourse)
]