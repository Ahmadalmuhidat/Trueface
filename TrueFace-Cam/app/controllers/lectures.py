import requests
import json

from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class LectureController:
  def __init__(self):
    from app.config.context import Context

    self._alerts_manager = AlertsManager()
    self._context = Context()
    self._configurations = Configurations()

  @error_handler
  def get_lectures_by_teacher(self) -> list[dict]:
    try:
      headers = {}
      token_data = self._configurations.get_token()
      if token_data:
        token = token_data.get("token") if isinstance(token_data, dict) else token_data
        headers["Authorization"] = f"Bearer {token}"

      response = requests.get(
        self._configurations.get_backend_endpoint() + "/lectures/get_by_teacher/",
        headers=headers,
        timeout=5
      )
      response.raise_for_status()
      return response.json()

    except requests.exceptions.Timeout:
      self._alerts_manager.error("Request timed out while loading lectures")
      return []
    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error while loading lectures: {str(e)}")
      return []
    except json.JSONDecodeError:
      self._alerts_manager.error("Invalid response format from server")
      return []
    except Exception as e:
      self._alerts_manager.error(f"Unexpected error while loading lectures: {str(e)}")
      return []
