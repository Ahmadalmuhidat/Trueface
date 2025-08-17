import cv2

from app.core.face_recognition_module import FaceRecognitionModule
from app.config.configrations import Configrations
from CTkMessagebox import CTkMessagebox
from app.core.logger import Logger
from app.config.context import Context

class FrameProcessor:
  def __init__(self):
    self.face_module = FaceRecognitionModule()
    self._config = Configrations()
    self._context = Context()
    self._logger = Logger()

    self._capture_thread_id = None

  def start(self, current_camera_index):
    if not self._context.get_current_class():
      self._alert("Error", "Please select a class from the settings")
      return

    self._capture_thread_id = self._config.frame_processing_executor.submit(self._capture_loop, current_camera_index)

  def stop(self):
    if self._capture_thread_id:
      try:
        self._capture_thread_id.result(timeout=5)
      except Exception as e:
        print("Error while waiting for capture to finish:", e)
      self._capture_thread_id = None

  def _capture_loop(self, current_camera_index):
    try:
      cap = cv2.VideoCapture(current_camera_index)
      cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
      cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

      frame_count = 0
      process_every = 5

      while not self._config.shutdown_event.is_set():
        ret, frame = cap.read()
        if not ret:
          continue
        frame_count += 1
        if frame_count % process_every == 0:
          self.face_module.analyze_camera_stream(frame)

      cap.release()

    except Exception as e:
      self._logger.log_exception(e)

  def _alert(self, title, message):
    CTkMessagebox(title=title, message=message, icon="cancel")
