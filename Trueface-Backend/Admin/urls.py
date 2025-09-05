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
  path('students/clear_lectures', lectures.ClearLecture),
  path('students/get_lectures', lectures.GetStudentLectures),
  path('students/remove_lecture', lectures.RemoveStudentFromLecture),
  path('students/add_lecture', lectures.AddStudentToLecture),

  # lectures
  path('lectures/remove', lectures.RemoveLecture),
  path('lectures/insert', lectures.InsertLecture),

  # courses
  path("courses/get_all", courses.GetCourses),
  path("courses/remove", courses.RemoveCourse),
  path("courses/insert", courses.InsertCourse),
  path('courses/get_lectures', lectures.GetLectures)
]