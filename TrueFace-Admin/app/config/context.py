from app.config.configrations import Configrations
from app.models.class_ import Class
from app.models.course import Course
from app.models.user import User
from app.models.student import Student

class Context():
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    # prevent re-initialization
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    self.courses = []
    self.classes = []
    self.users = []
    self.students = []

    self.config = Configrations()

  def get_courses(self):
    return self.courses
  
  def get_config(self):
    return self.config

  def get_classes(self):
    return self.classes

  def get_users(self):
    return self.users

  def get_students(self):
    return self.students

  def set_courses(self, courses):
    self.courses = [
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

  def set_classes(self, classes):
    self.classes = [
      Class(
        data['ID'],
        data['SubjectArea'],
        data['CatalogNBR'],
        data['AcademicCareer'],
        data['Course'], 
        data['OfferingNBR'], 
        data['StartTime'],
        data['EndTime'], 
        data['Section'], 
        data['Component'], 
        data['Campus'], 
        data['Name'], 
        data['InstructorType']
      ) for data in classes
    ]

  def set_users(self, users):
    self.users = [
      User(
        data['ID'],
        data['Name'],
        data['Email'],
        data['Role'], 
      ) for data in users
    ]

  def set_students(self, students):
    self.students = [
      Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName'], 
        data['Gender'],
        data['CreateDate']
      ) for data in students
    ]