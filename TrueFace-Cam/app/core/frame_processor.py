import cv2
import time

from app.config.configrations import Configrations
from app.config.context import Context
from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

class FrameProcessor:
  def __init__(self):
    self._config = Configrations()
    self._context = Context()
    self._alert = AlertsManager()

    self._capture_thread_id = None

    self._last_frame_time = 0
    self._frame_interval = 0.5

  @error_handler
  def _downscale_frame(self, frame):
    return cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

  @error_handler
  def start(self, current_camera_index):
    if not self._context.get_current_lecture():
      self._alert.info("Please select a class from the settings")
      return

    self._capture_thread_id = self._config.frame_processing_executor.submit(
      self._capture_loop,
      current_camera_index
    )

  @error_handler
  def _should_process_frame(self) -> bool:
    current_time = time.time()
    if current_time - self._last_frame_time < self._frame_interval:
      return False
    self._last_frame_time = current_time
    return True

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
        if not self._should_process_frame():
          return
        getattr(self._config, f"{self._config.current_recognizer}_module")

    cap.release()