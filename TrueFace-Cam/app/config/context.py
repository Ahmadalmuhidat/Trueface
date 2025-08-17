from app.config.configrations import Configrations
from app.interfaces.student import Student
from app.interfaces.attendance import Attendance
from app.interfaces.class_ import Class

class Context:
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

    # global data
    self._classes = []

    # global settings
    self.current_class = None

    # auth
    self._token = None
    self._config = Configrations()

  def get_students(self):
    return self.current_class.get_students()

  def set_students(self, students):
    for data in students:
      student = Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName'],
        data['Gender'],
        data['FaceID']
      )
      self.current_class.add_student(student)

  def get_attendance(self):
    return self.current_class.get_attendance()
  
  def set_attendance(self, attendance):
    for data in attendance:
      student = Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName']
      )
      student.confirm_attendance()

      attendance =  Attendance(student, data['Time'])
      self.current_class.add_attendance(attendance)

  def get_classes(self):
    return self._classes
  
  def set_classes(self, classes):
    self._classes = [
      Class(
        data['ID'],
        data['SubjectArea'],
        data['StartTime'],
        data['EndTime']
      ) for data in classes
    ]

  def get_current_class(self):
    return self.current_class
  
  def set_current_class(self, current_class: Class):
    self.current_class = current_class

  def get_jwt_token(self):
    return self._token
  
  def set_jwt_token(self, token):
    self._token = token

  def get_config(self):
    return self._config