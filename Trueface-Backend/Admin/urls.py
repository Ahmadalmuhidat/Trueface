from django.urls import path
from .controllers import lectures, users, students, courses

urlpatterns = [
  # users
  path('users/get_all', users.GetUsers),
  path('users/insert', users.InsertUser),
  path('users/remove', users.RemoveUser),
  path('users/update', users.UpdateUser),
  path('login', users.login),

  # students
  path('students/insert', students.InsertStudent),
  path('students/update', students.UpdateStudent),
  path('students/remove', students.RemoveStudent),
  path('students/get_all', students.GetAllStudents),
  path('students/get_lectures', students.GetStudentLectures),
  path('students/remove_lecture', students.RemoveStudentFromLecture),
  path('students/add_lecture', students.AddStudentToLecture),

  # lectures
  path('lectures/remove', lectures.RemoveLecture),
  path('lectures/update', lectures.UpdateLecture),
  path('lectures/insert', lectures.InsertLecture),

  # courses
  path("courses/get_all", courses.GetCourses),
  path("courses/remove", courses.RemoveCourse),
  path("courses/update", courses.UpdateCourse),
  path("courses/insert", courses.InsertCourse),
  path('courses/get_lectures', courses.GetLectures)
]
