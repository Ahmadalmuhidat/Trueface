import pickle
import base64

class Student:
  def __init__(self, student_id, first_name, middle_name, last_name, geneder = None, face_encode = None):
    # private
    self._face_encode = pickle.loads(base64.b64decode(face_encode))
    self._attendend = False

    # public
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = geneder
  
  def is_attended(self):
    return self._attendend
  
  def confirm_attendance(self):
    self._attendend = True
    
  def get_face_encode(self):
    return self._face_encode