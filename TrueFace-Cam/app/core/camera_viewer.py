from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager

class CameraViewer:
  def __init__(self):
    self._logger = Logger()
    self._alert = AlertsManager()

  def view_camera(self, index, available_cameras):
    try:
      camera = next((camera for camera in available_cameras if camera.get_index() == index), None)
      if camera:
        camera.view_stream()
      else:
        self._alert.pop_window(
          "No Camera Selected",
          "Please select camera before testing",
          "info"
        )

    except Exception as e:
      self._logger.log_exception(e)