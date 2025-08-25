from app.config.configrations import Configrations
from app.interfaces.student import Student
from app.interfaces.lecture import Lecture
from app.helper.error_handler import error_handler

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
    self._lectures = []
    self._current_lecture = None

    # auth
    self._token = None

    self._config = Configrations()

  def get_students(self):
    return self._current_lecture.get_students()

  @error_handler
  def set_students(self, students):
    for data in students:
      student = Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName'],
        data['Gender'],
        data['FaceID'],
        data["Time"]
      )
      self._current_lecture.add_student(student)

  def get_lectures(self):
    return self._lectures

  @error_handler
  def set_lectures(self, lectures):
    self._lectures = [
      Lecture(
        data['ID'],
        data['SubjectArea'],
        data['StartTime'],
        data['EndTime']
      ) for data in lectures
    ]

  def get_current_lecture(self):
    return self._current_lecture
  
  def set_current_lecture(self, current_lecture: Lecture):
    self._current_lecture = current_lecture

  def get_jwt_token(self):
    return self._token
  
  def set_jwt_token(self, token):
    self._token = token