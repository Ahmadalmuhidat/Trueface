import cv2
import time
import numpy

from app.config.configurations import Configurations
from app.config.context import Context
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class FrameProcessor:
  def __init__(self) -> None:
    self._config = Configurations()
    self._context = Context()
    self._alert = AlertsManager()

    self._capture_thread_id = None
    self._last_frame_time = 0
    self._frame_interval = 0.3
    self._frame_skip = 3
    self._max_processing_size = (320, 240)

  @error_handler
  def _downscale_frame(self, frame: numpy.ndarray) -> numpy.ndarray:
    return cv2.resize(frame, self._max_processing_size, interpolation=cv2.INTER_AREA)

  @error_handler
  def start(self, current_camera_index: int) -> None:
    if not self._context.get_current_lecture():
      self._alert.info("Please select a lecture from the settings")
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
  def stop(self) -> None:
    if self._capture_thread_id:
      try:
        self._capture_thread_id.result(timeout=5)

      except Exception as e:
        print("Error while waiting for capture to finish:", e)
      self._capture_thread_id = None

  @error_handler
  def _capture_loop(self, current_camera_index: int) -> None:
    cap = cv2.VideoCapture(current_camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 15)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    frame_count = 0

    try:
      while not self._config.shutdown_event.is_set():
        ret, frame = cap.read()
        if not ret:
          continue
        
        frame_count += 1
        if frame_count % self._frame_skip == 0:
          if not self._should_process_frame():
            continue
          
          small_frame = self._downscale_frame(frame)
          recognizer_module = getattr(self._config, f"{self._config.current_recognizer}_module")
          recognizer_module.process_camera_stream(small_frame)

    finally:
      cap.release()
      cv2.destroyAllWindows()