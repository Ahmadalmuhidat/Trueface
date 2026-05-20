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

      params = {
        "current_lecture": self._context.get_current_lecture().lecture_id
      }

      headers = {}
      token_data = self._configurations.get_token()
      if token_data:
        token = token_data.get("token") if isinstance(token_data, dict) else token_data
        headers["Authorization"] = f"Bearer {token}"

      response = requests.get(
        self._configurations.get_backend_endpoint() + "/students/get_by_lecture/",
        params=params,
        headers=headers
      )
      response.raise_for_status()
      return response.json()

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
