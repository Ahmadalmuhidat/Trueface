from app.config.configurations import Configurations
from app.interfaces.course import Course
from app.interfaces.user import User
from app.interfaces.student import Student
from app.controllers.users import UsersController
from app.controllers.students import StudentsController
from app.controllers.courses import CoursesController

class Context():
  # singleton pattern
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    self._courses = []
    self._users = []
    self._students = []
    self._current_course = None
    self._current_student = None
    self._config = Configurations()

    # controllers
    self._users_controller = UsersController()
    self._students_controller = StudentsController()
    self._courses_controller = CoursesController()
  
  def fetch_users(self) -> None:
    users = self._users_controller.fetch_users()
    self.set_users(users)
  
  def fetch_students(self) -> None:
    students = self._students_controller.fetch_students()
    self.set_students(students)

  def fetch_courses(self) -> None:
    courses = self._courses_controller.fetch_courses()
    self.set_courses(courses)

  def set_current_student(self, student: Student) -> None:
    self._current_student = student
  
  def get_current_student(self) -> Student:
    return self._current_student

  def set_current_course(self, course: Course) -> None:
    self._current_course = course
  
  def get_current_course(self) -> Course:
    return self._current_course

  def set_courses(self, courses: list[dict]) -> None:
    self._courses = [
      Course(
        data.get('id'),
        data.get('title'),
        data.get('credit'),
        data.get('maximum_units'), 
        data.get('long_course_title'),
        data.get('offering_nbr'),
        data.get('academic_group'), 
        data.get('subject_area'),
        data.get('catalog_nbr'),
        data.get('campus'), 
        data.get('academic_organization'),
        data.get('component')
      ) for data in courses
    ]

  def get_courses(self) -> list[Course]:
    return self._courses

  def add_course(self, course: Course) -> None:
    self._courses.append(course)

  def set_users(self, users: list[dict]) -> None:
    self._users = [
      User(
        data.get('id'),
        data.get('name'),
        data.get('email'),
        data.get('role'), 
      ) for data in users
    ]

  def get_users(self) -> list[User]:
    return self._users

  def add_user(self, user: User) -> None:
    self._users.append(user)

  def set_students(self, students: list[dict]) -> None:
    self._students = [
      Student(
        data.get('id'),
        data.get('first_name'),
        data.get('middle_name'),
        data.get('last_name'), 
        data.get('gender'),
        data.get('create_date')
      ) for data in students
    ]

  def get_students(self) -> list[Student]:
    return self._students

  def add_student(self, stduent: Student) -> None:
    self._students.append(stduent)
