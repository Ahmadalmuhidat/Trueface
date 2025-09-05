import base64
import face_recognition
import pickle
import threading

from app.interfaces.lecture import Lecture
from typing import List
from app.helper.error_handler import error_handler

class Student:
  def __init__(
    self, student_id: str, first_name: str, middle_name: str,
    last_name: str, gender: str, create_date: str = None, picture: str = None
  ):
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = gender
    self.create_date = create_date
    self.picture = picture

    self._lectures = []

    threading.Thread(target=self.fetch_lectures).start()

  @error_handler
  def fetch_lectures(self):
    from app.controllers.students import get_lectures_by_student
    
    self._lectures.clear()

    for lecture in get_lectures_by_student(self):
      lecture = Lecture(
        class_id=lecture["ID"],
        subject_area=lecture["SubjectArea"],
        start_time=lecture["StartTime"],
        end_time=lecture["EndTime"],
        day=lecture["Day"]
      )
      self._lectures.append(lecture)

  def get_lectures(self) -> List[Lecture]:
    return self._lectures

  def add_lecture(self, lecture: Lecture):
    self._lectures.append(lecture)

  def search_leacture(self, term: str):
    return [lecture for lecture in self._lectures if term == lecture.lecture_id or term in lecture.subject_area]

  @error_handler
  def remove_lecture(self, lecture_id):
    self._lectures = [lecture for lecture in self._lectures if lecture.lecture_id != lecture_id]

  @error_handler
  def get_face_encode(self):
    load_stored_image = face_recognition.load_image_file(self.picture)
    return base64.b64encode(pickle.dumps(face_recognition.face_encodings(load_stored_image)[0])).decode('utf-8')

  @error_handler
  def check_face_in_image(self):
    load_stored_image = face_recognition.load_image_file(self.picture)
    face_found = face_recognition.face_locations(load_stored_image)

    if face_found:
      return True
    else:
      return False