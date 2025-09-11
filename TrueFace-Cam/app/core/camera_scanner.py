from cv2_enumerate_cameras import enumerate_cameras
from app.interfaces.camera import Camera
from app.helper.alerts_manager import AlertsManager
from typing import List
from app.helper.error_handler import error_handler

class CameraScanner:
  def __init__(self):
    # private
    self._alert = AlertsManager()

    self._available_cameras = []
    self.found_active_connected_camera = False

  @error_handler
  def scan_connected_cameras(self):
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
      self._alert.warrning("Did not find any connected camera")

  def get_available_cameras(self) -> List[Camera]:
    return self._available_cameras