import requests
import json

from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class AuthController:
  def __init__(self):
    self._alerts_manager = AlertsManager()

  @error_handler
  def login(self, email: str, password: str) -> dict:
    try:
      from app.config.configurations import Configurations
      config = Configurations()

      data = {
        "email": email,
        "password": password
      }
      response = requests.post(f"{config.get_backend_endpoint()}/auth/login/", json=data)
      response.raise_for_status()
      return response.json()

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return None
