from app.interfaces.student import Student
from app.interfaces.lecture import Lecture
from app.utils.error_handler import error_handler
from typing import List
from app.controllers.students import StudentController
from app.controllers.lectures import LectureController

class Context:
  # Singleton pattern
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

    self._lectures = []
    self._current_lecture = None
    self._token = None

    self._student_controller = StudentController()
    self._lecture_controller = LectureController()

  def fetch_lectures(self) -> None:
    lectures = self._lecture_controller.get_lectures_by_teacher()
    self.set_lectures(lectures)
  
  def fetch_students(self) -> None:
    if not self._current_lecture:
      return

    students = self._student_controller.get_students_by_lecture()
    self.set_students(students)

  def get_students(self) -> list[Student]:
    if not self._current_lecture:
      return []

    return self._current_lecture.get_students()

  def set_students(self, students: list[dict]) -> None:
    if not self._current_lecture:
      return

    self._current_lecture.clear_students()
    for data in students:
      student = Student(
        data['id'],
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['gender'],
        data['face_id'],
        data["time"]
      )
      self._current_lecture.add_student(student)

  def get_lectures(self) -> list[Lecture]:
    return self._lectures

  def set_lectures(self, lectures: list[dict]) -> None:
    self._lectures.clear()
    self._lectures = [
      Lecture(
        data['id'],
        data['subject_area'],
        data['start_time'],
        data['end_time']
      ) for data in lectures
    ]

  def get_current_lecture(self) -> Lecture:
    return self._current_lecture
  
  def set_current_lecture(self, current_lecture: Lecture) -> None:
    self._current_lecture = current_lecture

  def get_jwt_token(self) -> str:
    return self._token
  
  def set_jwt_token(self, token: str) -> None:
    self._token = token
