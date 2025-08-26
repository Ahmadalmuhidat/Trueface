import pickle
import base64

from datetime import datetime

class Student:
  def __init__(self, student_id: str, first_name: str, middle_name: str, last_name: str, geneder: str, face_encode: str, Time: str = None):
    # private
    self._face_encode = pickle.loads(base64.b64decode(face_encode)) if face_encode else None

    # public
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = geneder
    self.time = Time
  
  def is_attended(self):
    return False if not self.time else True
  
  def confirm_attendance(self):
     self.time = datetime.now()
    
  def get_face_encode(self):
    return self._face_encode