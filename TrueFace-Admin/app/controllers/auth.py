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

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/auth/login/",
        json=data
      )
      response.raise_for_status()
      return response.json()

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return None
