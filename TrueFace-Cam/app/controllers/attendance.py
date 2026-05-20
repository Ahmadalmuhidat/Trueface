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
  def insert_attendance(self, student_id: str, student_name: str) -> bool:
    try:
      current_lecture = self._context.get_current_lecture()
      if not current_lecture:
        return False

      data = {
        "student_id": student_id,
        "lecture_field": current_lecture.lecture_id
      }

      headers = {}
      token_data = self._configurations.get_token()
      if token_data:
        token = token_data.get("token") if isinstance(token_data, dict) else token_data
        headers["Authorization"] = f"Bearer {token}"

      response = requests.post(
        self._configurations.get_backend_endpoint() + "/attendance/",
        json=data,
        headers=headers,
        timeout=10
      )
      response.raise_for_status()
      self._alerts_manager.success("{} has been signed".format(student_name))
      return True

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False