from typing import List
from app.interfaces.student import Student

class Lecture:
  def __init__(self, class_id = None, subject_area = None, start_time = None, end_time = None):
    # private
    self._students = []

    # public
    self.class_id = class_id
    self.subject_area = subject_area
    self.start_time = start_time
    self.end_time = end_time

  def add_student(self, student: Student):
    self._students.append(student)

  def get_students(self) -> List[Student]:
    return self._students