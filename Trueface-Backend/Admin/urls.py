from django.urls import path
from .controllers import users, students, classes, courses

urlpatterns = [
  # users
  path('insert_user', users.InsertUser),
  path('get_users', users.GetUsers),
  path('search_user', users.SearchUser),
  path('remove_user', users.RemoveUser),
  path('login', users.login),

  # students
  path('insert_student', students.InsertStudent),
  path('remove_student', students.RemoveStudent),
  path('get_all_students', students.GetAllStudents),
  path('search_student', students.SearchStudent),
  path('get_students_count', students.GetStudentsCount),
  path('check_duplicated_student_id', students.CheckDuplicatedStudentId), # remove

  # classes
  path('get_classes', classes.GetClasses),
  path('search_class', classes.SearchClass),
  path('remove_class', classes.RemoveClass),
  path('insert_class_student_relation', classes.InsertClassStudentRelation),
  path('clear_class_student_relation', classes.ClearClassStudentRelation),
  path('insert_class', classes.InsertClass),
  path('get_classes_student_relation', classes.GetClassesStudentRelation),
  path('remove_class_student_relation', classes.RemoveClassStudentRelation),
  path('get_classes_for_selection', classes.GetClassesForSelection), # remove

  # courses
  path("get_courses", courses.GetCourses),
  path("search_courses", courses.SearchCourses),
  path("remove_course", courses.RemoveCourse),
  path("insert_course", courses.InsertCourse)
]