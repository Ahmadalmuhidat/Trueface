from abc import ABC, abstractmethod
from app.interfaces.student import Student

class Recognizer(ABC):
  def __init__(self):
    super().__init__()

  @abstractmethod
  def analyze_camera_stream(self, frame) -> bool:
    """Analyze a frame from the camera stream."""
    pass

  @abstractmethod
  def _detect_faces(self, frame):
    """Detect faces in the given frame."""
    pass

  @abstractmethod
  def _get_known_encodings(self):
    """Return a list of known face encodings."""
    pass

  @abstractmethod
  def _encode_faces(self, frame, face_locations):
    """Encode faces detected in the frame."""
    pass

  @abstractmethod
  def _compare_faces(self, known_encodings, cam_face_encodings):
    """Compare known encodings with current frame encodings."""
    pass

  @abstractmethod
  def _process_matches(self, matches):
    """Process the matches found in comparison."""
    pass

  @abstractmethod
  def _record_attendance(self, student: Student):
    """Record attendance for the given student."""
    pass