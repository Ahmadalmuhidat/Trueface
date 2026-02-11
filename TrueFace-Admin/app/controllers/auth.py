import json
import requests

from app.utils.alerts_manager import AlertsManager
from app.config.configurations import Configurations
from app.utils.error_handler import error_handler
from app.utils.session_manager import get_session

class AuthController:
  def __init__(self):
    self._session = get_session()
    self._configurations = Configurations()
    self._alerts_manager = AlertsManager()

  @error_handler
  def login(self, email: str, password: str) -> dict:
    try:
      data = {
        "email": email,
        "password": password
      }

      response = self._session.get(
        self._configurations.get_backend_endpoint() + "/login",
        params=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        return response_data.get("data")
      else:
        message = response_data.get("error")
        self._alerts_manager.error(
          message=message if message else "Something went wrong while checking user info",
        )
        return None

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return None
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return None
