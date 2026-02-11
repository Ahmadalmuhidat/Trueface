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
      data = {
        "email": email,
        "password": password
      }
      response = requests.get("http://localhost:8000/admin/login", params = data).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        return response.get("data")
      else:
        message = response.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while logging in")
        return None

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return None
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return None
