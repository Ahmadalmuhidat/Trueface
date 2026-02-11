import requests
import json

from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class StudentController:
  def __init__(self):
    from app.config.context import Context

    self._alerts_manager = AlertsManager()
    self._context = Context()
    self._configurations = Configurations()

  @error_handler
  def get_students_by_lecture(self) -> list[dict]:
    try:
      if not self._context.get_current_lecture():
        return []

      data = {
        "current_lecture": self._context.get_current_lecture().lecture_id
      }

      response = requests.get(
        self._configurations.get_backend_endpoint() + "/students/get_by_lecture",
        params = data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        return response_data.get("data")
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message = message if message else "Something went wrong while getting the students")
        return []

    except requests.exceptions.Timeout:
      self._alerts_manager.error("Request timed out while loading students")
      return []
    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error while loading students: {str(e)}")
      return []
    except json.JSONDecodeError:
      self._alerts_manager.error("Invalid response format from server")
      return []
    except Exception as e:
      self._alerts_manager.error(f"Unexpected error while loading students: {str(e)}")
      return []
