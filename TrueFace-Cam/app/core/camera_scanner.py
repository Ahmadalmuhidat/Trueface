from cv2_enumerate_cameras import enumerate_cameras
from app.interfaces.camera import Camera
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler
from typing import List

class CameraScanner:
  def __init__(self) -> None:
    self.found_active_connected_camera = False

    self._alert = AlertsManager()
    self._available_cameras = []

  @error_handler
  def scan_connected_cameras(self) -> None:
    self._available_cameras.clear()
    found_any = False
    for camera in enumerate_cameras():
      cam = Camera(camera.index, camera.name)
      if cam.test_if_working():
        self._available_cameras.append(cam)
        found_any = True
    self.found_active_connected_camera = found_any

    if found_any:
      self._alert.success("Done Scanning Connecetd cameras")
    else:
      self._alert.warning("Did not find any connected camera")

  def get_available_cameras(self) -> List[Camera]:
    return self._available_cameras