from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler
from typing import List
from app.interfaces.camera import Camera

class CameraViewer:
  def __init__(self) -> None:
    self._alert = AlertsManager()

  @error_handler
  def view_camera(self, index: int, available_cameras: List[Camera]) -> None:
    camera = next((camera for camera in available_cameras if camera.get_index() == index), None)
    if camera:
      camera.view_stream()
    else:
      self._alert.info("Please select camera before testing")
