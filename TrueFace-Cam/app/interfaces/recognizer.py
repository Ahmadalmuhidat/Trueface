import numpy

from typing import List, Tuple
from abc import ABC, abstractmethod
from app.interfaces.student import Student

class Recognizer(ABC):
  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def process_camera_stream(self, frame) -> bool:
    pass

  @abstractmethod
  def _detect_faces(self, frame) -> List[Tuple[int, int, int, int]]:
    pass

  @abstractmethod
  def _get_known_encodings(self) -> List[numpy.ndarray]:
    pass

  @abstractmethod
  def _encode_faces(self, frame, face_locations) -> List[numpy.ndarray]:
    pass

  @abstractmethod
  def _compare_faces(self, known_encodings, cam_face_encodings) -> List[bool]:
    pass

  @abstractmethod
  def _process_matches(self, matches) -> None:
    pass

  @abstractmethod
  def _record_attendance(self, student: Student) -> None:
    pass
