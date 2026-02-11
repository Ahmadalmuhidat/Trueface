from typing import List
from app.interfaces.student import Student

class Lecture:
  def __init__(
    self, lecture_id: str = None, subject_area: str = None,
    start_time: str = None, end_time: str = None
  ) -> None:
    # private
    self._students: list[Student] = []

    # public
    self.lecture_id = lecture_id
    self.subject_area = subject_area
    self.start_time = start_time
    self.end_time = end_time

  def add_student(self, student: Student) -> None:
    self._students.append(student)

  def get_students(self) -> List[Student]:
    return self._students

  def clear_students(self) -> None:
    self._students.clear()
