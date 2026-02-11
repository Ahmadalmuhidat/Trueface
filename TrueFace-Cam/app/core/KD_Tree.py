import face_recognition
import winsound
import numpy

from typing import List, Tuple
from threading import Lock, Thread
from sklearn.neighbors import KDTree
from app.config.context import Context
from app.interfaces.student import Student
from app.controllers.attendance import AttendanceController
from app.utils.error_handler import error_handler
from app.interfaces.recognizer import Recognizer

class KD_Tree_Module(Recognizer):
  def __init__(self) -> None:
    super().__init__()
    from app.config.configurations import Configurations

    self.attendace_controller = AttendanceController()

    self._context = Context()
    self._config = Configurations()
    self._scan_lock = Lock()

    self._kd_tree = None
    self._student_encodings = None
    self._tolerance = 0.5
    self._tree_built = False
    self._last_student_count = 0

  def _build_kd_tree(self) -> None:
    students = self._context.get_students()
    if not students:
      return

    self._student_encodings = numpy.array([student.get_face_encode() for student in students])
    self._kd_tree = KDTree(self._student_encodings)
    self._tree_built = True
    self._last_student_count = len(students)
  
  def _ensure_tree_built(self) -> None:
    current_students = self._context.get_students()
    current_count = len(current_students)
    
    if not self._tree_built or current_count != self._last_student_count:
      self._build_kd_tree()

  @error_handler
  def process_camera_stream(self, frame: numpy.ndarray) -> None:
    self._ensure_tree_built()
    
    face_locations = self._detect_faces(frame)
    if not face_locations or self._kd_tree is None:
      return

    cam_face_encodings = self._encode_faces(frame, face_locations)
    if cam_face_encodings:
      matches = self._compare_faces(self._student_encodings, cam_face_encodings[0])
      self._process_matches(matches)

  @error_handler
  def _detect_faces(self, frame: numpy.ndarray) -> List[Tuple[int, int, int, int]]:
    model = "hog" if self._config.get_processing_mode() == "CPU" else "cnn"
    return face_recognition.face_locations(frame, model=model)

  def _get_known_encodings(self) -> List[numpy.ndarray]:
    return self._student_encodings

  @error_handler
  def _encode_faces(self, frame: numpy.ndarray, face_locations: List[Tuple[int, int, int, int]]) -> List[numpy.ndarray]:
    return face_recognition.face_encodings(frame, face_locations)

  @error_handler
  def _compare_faces(self, known_encodings: List[numpy.ndarray], cam_face_encoding: numpy.ndarray) -> List[bool]:
    distances, indices = self._kd_tree.query([cam_face_encoding], k=1)
    nearest_idx = indices[0][0]
    distance = distances[0][0]

    match = distance < self._tolerance
    matches = [False] * len(known_encodings)
    if match:
      matches[nearest_idx] = True

    return matches

  @error_handler
  def _process_matches(self, matches: List[bool]) -> None:
    students = self._context.get_students()
    for i, match in enumerate(matches):
      if match and i < len(students):
        with self._scan_lock:
          student = students[i]
          if not student.is_attended():
            self._record_attendance(student)
            Thread(target=winsound.Beep, args=(2500, 500)).start()

  @error_handler
  def _record_attendance(self, student: Student) -> None:
    self._config.frame_processing_executor.submit(
      self.attendace_controller.insert_attendance,
      student.student_id,
      f"{student.first_name} {student.last_name}"
    )
    student.confirm_attendance()
