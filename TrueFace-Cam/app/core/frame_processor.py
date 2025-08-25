import cv2

from app.core.face_recognition_module import FaceRecognitionModule
from app.config.configrations import Configrations
from app.config.context import Context
from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

class FrameProcessor:
  def __init__(self):
    self.face_module = FaceRecognitionModule()
    self._config = Configrations()
    self._context = Context()
    self._alert = AlertsManager()

    self._capture_thread_id = None

  @error_handler
  def start(self, current_camera_index):
    if not self._context.get_current_lecture():
      self._alert.pop_window(
        "Error",
        "Please select a class from the settings",
        "info"
      )
      return

    self._capture_thread_id = self._config.frame_processing_executor.submit(self._capture_loop, current_camera_index)

  @error_handler
  def stop(self):
    if self._capture_thread_id:
      try:
        self._capture_thread_id.result(timeout=5)

      except Exception as e:
        print("Error while waiting for capture to finish:", e)
      self._capture_thread_id = None

  @error_handler
  def _capture_loop(self, current_camera_index):
    cap = cv2.VideoCapture(current_camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    process_every = 10

    while not self._config.shutdown_event.is_set():
      ret, frame = cap.read()
      if not ret:
        continue
      frame_count += 1
      if frame_count % process_every == 0:
        self.face_module.analyze_camera_stream(frame)

    cap.release()
