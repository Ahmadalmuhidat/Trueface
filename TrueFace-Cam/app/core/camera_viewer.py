from app.interfaces.camera import Camera
from app.core.logger import Logger
from typing import List

class CameraViewer:
  def __init__(self):
    self._logger = Logger()

  def view_camera(self, index, cameras: List[Camera]):
    try:
      camera = next((camera for camera in cameras if camera.get_index() == index), None)
      if camera:
        camera.view_stream()
      else:
        self._alert("No Camera Selected", "Please select camera before testing")

    except Exception as e:
      self._logger.log_exception(e)