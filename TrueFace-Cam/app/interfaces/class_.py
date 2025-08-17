from typing import List
from app.interfaces.student import Student
from app.interfaces.attendance import Attendance

class Class:
  def __init__(self, class_id = None, subject_area = None, start_time = None, end_time = None):
    # private
    self._students = []
    self._attendance = []

    # public
    self.class_id = class_id
    self.subject_area = subject_area
    self.start_time = start_time
    self.end_time = end_time

  def add_student(self, student: Student):
    self._students.append(student)

  def get_students(self) -> List[Student]:
    return self._students

  def add_attendance(self, attendance: Attendance):
    self._attendance.append(attendance)

  def get_attendance(self) -> List[Attendance]:
    return self._attendance