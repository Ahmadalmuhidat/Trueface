import requests
import json
import threading
import time

from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class AttendanceController:
  def __init__(self):
    from app.config.context import Context

    self._context = Context()
    self._configurations = Configurations()
    self._alerts_manager = AlertsManager()

  @error_handler
  def insert_attendance(student_id: str, student_name: str) -> bool:
    try:
      current_lecture = self._context.get_current_lecture()
      if not current_lecture:
        return False

      data = {
        "student_id": student_id,
        "current_lecture": current_lecture.lecture_id
      }

      response = requests.post(
        self._configurations.get_backend_endpoint() + "/attendance/batch_insert",
        data=data,
        timeout=10
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        self._alerts_manager.success("{} has been signed".format(student_name))
        return True
      else:
        message = response.get("error", "Something went wrong while inserting attendance")
        self._alerts_manager.error(message)
      return False

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False