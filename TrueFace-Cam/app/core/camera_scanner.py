from cv2_enumerate_cameras import enumerate_cameras
from app.interfaces.camera import Camera
from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager
from typing import List

class CameraScanner:
  def __init__(self):
    # Private
    self._logger = Logger()
    self._alert = AlertsManager()

    self._available_cameras = []
    self.found_active_connected_camera = False

  def scan_connected_cameras(self):
    try:
      self._available_cameras.clear()
      found_any = False
      for camera in enumerate_cameras():
        cam = Camera(camera.index, camera.name)
        if cam.test_if_working():
          self._available_cameras.append(cam)
          found_any = True
      self.found_active_connected_camera = found_any

      self._alert.pop_window(
        "Scanning Status",
        "Done Scanning Connecetd cameras" if found_any else "Did not find any connected camera",
        "check" if found_any else "warning"
      )

    except Exception as e:
      self._logger.log_exception(e)

  def get_available_cameras(self) -> List[Camera]:
    return self._available_cameras