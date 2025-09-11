from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

class CameraViewer:
  def __init__(self):
    self._alert = AlertsManager()

  @error_handler
  def view_camera(self, index, available_cameras):
    camera = next((camera for camera in available_cameras if camera.get_index() == index), None)
    if camera:
      camera.view_stream()
    else:
      self._alert.info("Please select camera before testing")
