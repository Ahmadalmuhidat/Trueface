from app.config.configrations import Configrations
from app.interfaces.course import Course
from app.interfaces.user import User
from app.interfaces.student import Student

class Context():
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

    self._config = Configrations()

  def set_current_student(self, student):
    self._current_student = student
  
  def get_current_student(self) -> Student:
    return self._current_student

  def set_current_course(self, course):
    self._current_course = course
  
  def get_current_course(self) -> Course:
    return self._current_course

  def set_courses(self, courses):
    self._courses = [
      Course(
        data['ID'],
        data['Title'],
        data['Credit'],
        data['MaximumUnits'], 
        data['LongCourseTitle'],
        data['OfferingNBR'],
        data['AcademicGroup'], 
        data['SubjectArea'],
        data['CatalogNBR'],
        data['Campus'], 
        data['AcademicOrganization'],
        data['Component']
      ) for data in courses
    ]

  def get_courses(self):
    return self._courses

  def add_course(self, course: Course):
    self._courses.append(course)

  def set_users(self, users):
    self._users = [
      User(
        data['ID'],
        data['Name'],
        data['Email'],
        data['Role'], 
      ) for data in users
    ]

  def get_users(self):
    return self._users

  def add_user(self, user: User):
    self._users.append(user)

  def set_students(self, students):
    self._students = [
      Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName'], 
        data['Gender'],
        data['CreateDate']
      ) for data in students
    ]

  def get_students(self):
    return self._students

  def add_student(self, stduent: Student):
    self._students.append(stduent)
