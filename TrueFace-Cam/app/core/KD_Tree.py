import face_recognition
import winsound
import numpy as np

from threading import Lock, Thread
from sklearn.neighbors import KDTree

from app.config.context import Context
from app.interfaces.student import Student
from app.controllers.attendance import insert_attendance
from app.helper.error_handler import error_handler
from app.interfaces.recognizer import Recognizer

class KD_Tree_Module(Recognizer):
  def __init__(self) -> None:
    super().__init__()

    from app.config.configrations import Configrations

    self._context = Context()
    self._config = Configrations()
    self._scan_lock = Lock()

    # KD-Tree related
    self._kd_tree = None
    self._student_encodings = None
    self._tolerance = 0.5

  def _build_kd_tree(self):
    students = self._context.get_students()
    if not students:
      return

    self._student_encodings = np.array([student.get_face_encode() for student in students])
    self._kd_tree = KDTree(self._student_encodings)

  @error_handler
  def analyze_camera_stream(self, frame) -> bool:
    face_locations = self._detect_faces(frame)
    if not face_locations or self._kd_tree is None:
      return

    cam_face_encodings = self._encode_faces(frame, face_locations)
    if cam_face_encodings:
      matches = self._compare_faces(self._student_encodings, cam_face_encodings[0])
      self._process_matches(matches)

  @error_handler
  def _detect_faces(self, frame):
    model = "hog" if self._config.get_processing_mode() == "CPU" else "cnn"
    return face_recognition.face_locations(frame, model=model)

  def _get_known_encodings(self):
    return self._student_encodings

  @error_handler
  def _encode_faces(self, frame, face_locations):
    return face_recognition.face_encodings(frame, face_locations)

  @error_handler
  def _compare_faces(self, known_encodings, cam_face_encoding):
    distances, indices = self._kd_tree.query([cam_face_encoding], k=1)
    nearest_idx = indices[0][0]
    distance = distances[0][0]

    # Compare with tolerance
    match = distance < self._tolerance
    matches = [False] * len(known_encodings)
    if match:
      matches[nearest_idx] = True

    return matches

  @error_handler
  def _process_matches(self, matches):
    for i, match in enumerate(matches):
      if match:
        with self._scan_lock:
          student = self._context.get_students()[i]
          if not student.is_attended():
            self._record_attendance(student)
            Thread(target=winsound.Beep, args=(2500, 500)).start()

  @error_handler
  def _record_attendance(self, student: Student):
    self._config.frame_processing_executor.submit(
      insert_attendance,
      student.student_id,
      f"{student.first_name} {student.last_name}"
    )
    student.confirm_attendance()
