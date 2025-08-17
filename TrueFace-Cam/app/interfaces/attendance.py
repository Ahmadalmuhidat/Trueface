from app.interfaces.student import Student

class Attendance:
  def __init__(self, student: Student, time):
    self._student = student
    self._time = time
  
  def get_student(self):
    return self._student
  
  def get_time(self):
    return self._time
