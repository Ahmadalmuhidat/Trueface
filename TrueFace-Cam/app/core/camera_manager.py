from app.core.camera_scanner import CameraScanner
from app.core.camera_viewer import CameraViewer
from app.core.frame_processor import FrameProcessor
from app.config.context import Context
from app.core.face_recognition_module import FaceRecognitionModule
from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler
from app.interfaces.camera import Camera
from typing import List

class CameraManager:
  # singleton pattern
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # camera components
    self.camera_scanner = CameraScanner()
    self.camera_viewer = CameraViewer()
    self.frame_processor = FrameProcessor()

    # modules
    self._context = Context()
    self._config = Configurations()
    self._face_recognition_module = FaceRecognitionModule()
    self._alert = AlertsManager()

    # camera state
    self._current_camera_index = 0
    self._capturing_is_active = False

  def set_current_camera_index(self, index: int) -> None:
    self._current_camera_index = index

  def get_current_camera_index(self) -> int:
    return self._current_camera_index

  def set_capturing(self, value: bool) -> None:
    self._capturing_is_active = value

  def is_capturing(self) -> bool:
    return self._capturing_is_active

  def scan_connected_cameras(self) -> List[Camera]:
    self.camera_scanner.scan_connected_cameras()
    return self.camera_scanner.get_available_cameras()

  @error_handler
  def view_current_camera_stream(self) -> None:
    if not self.camera_scanner.found_active_connected_camera:
      self._alert.error("Please make sure you connected at least one camera")
      return

    if self.is_capturing():
      self._alert.error("Please make sure the camera is not already operating")
      return

    self.camera_viewer.view_camera(self._current_camera_index, self.camera_scanner._available_cameras)

  @error_handler
  def start_capturing(self) -> None:
    if self.is_capturing():
      self._alert.info("Please make sure the camera is not already operating")
      return

    if not self.camera_scanner.found_active_connected_camera:
      self._alert.error("Failed to find active cameras")
      return

    self.set_capturing(True)
    self._config.shutdown_event.clear()
    self.frame_processor.start(self.get_current_camera_index())

  @error_handler
  def stop_capturing(self) -> None:
    if not self.is_capturing():
      self._alert.error("Camera is not capturing")
      return
    
    self.set_capturing(False)
    self._config.shutdown_event.set()
    self.frame_processor.stop()
