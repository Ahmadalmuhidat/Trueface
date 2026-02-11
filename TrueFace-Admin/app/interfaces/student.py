from __future__ import annotations
import base64
import face_recognition
import pickle
import threading
import hashlib
import os

from app.interfaces.lecture import Lecture
from typing import List
from app.utils.error_handler import error_handler

class Student:  
  def __init__(
    self, student_id: str, first_name: str, middle_name: str,
    last_name: str, gender: str, create_date: str = None, picture: str = None
  ) -> None:
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = gender
    self.create_date = create_date
    self.picture = picture

    self._lectures: list[Lecture] = []
    self._face_encoding = None
    self._cached_encoding = False

    threading.Thread(target=self.fetch_lectures, daemon=True).start()

  @error_handler
  def fetch_lectures(self) -> None:
    from app.controllers.students import StudentsController
    
    self._lectures.clear()

    for lecture in StudentsController().fetch_lectures_by_student(self):
      lecture_id = lecture.get("id")
      subject_area = lecture.get("subject_area")
      start_time = lecture.get("start_time")
      end_time = lecture.get("end_time")
      day = lecture.get("day")
      
      lecture_obj = Lecture(
        class_id=lecture_id,
        subject_area=subject_area,
        start_time=start_time,
        end_time=end_time,
        day=day
      )
      self._lectures.append(lecture_obj)

  def get_lectures(self) -> List[Lecture]:
    return self._lectures

  def add_lecture(self, lecture: Lecture) -> None:
    self._lectures.append(lecture)

  def search_lecture(self, term: str) -> List[Lecture]:
    return [lecture for lecture in self._lectures if term == lecture.lecture_id or term in lecture.subject_area]

  @error_handler
  def remove_lecture(self, lecture_id: str) -> None:
    self._lectures = [lecture for lecture in self._lectures if lecture.lecture_id != lecture_id]

  def _get_image_hash(self, image_path: str) -> str:
    try:
      stat = os.stat(image_path)
      with open(image_path, 'rb') as f:
        content = f.read()
      return hashlib.md5(content + str(stat.st_mtime).encode()).hexdigest()

    except (OSError, IOError):
      return hashlib.md5(image_path.encode()).hexdigest()

  @error_handler
  def get_face_encode(self) -> str:
    if self._cached_encoding and self._face_encoding:
      return self._face_encoding
    
    if not self.picture or not os.path.exists(self.picture):
      raise ValueError("Picture file not found")
    
    try:
      load_stored_image = face_recognition.load_image_file(self.picture)
      face_encodings = face_recognition.face_encodings(load_stored_image)
      
      if not face_encodings:
        raise ValueError("No face found in the image")
      
      face_encoding = face_encodings[0]
      encoding_str = base64.b64encode(pickle.dumps(face_encoding)).decode('utf-8')
      
      self._face_encoding = encoding_str
      self._cached_encoding = True
      
      return encoding_str

    except Exception as e:
      raise ValueError(f"Failed to process face encoding: {str(e)}")

  @error_handler
  def check_face_in_image(self) -> bool:
    if not self.picture or not os.path.exists(self.picture):
      return False

    try:
      load_stored_image = face_recognition.load_image_file(self.picture)
      face_found = face_recognition.face_locations(load_stored_image)
      has_face = len(face_found) > 0
      return has_face

    except Exception:
      return False
