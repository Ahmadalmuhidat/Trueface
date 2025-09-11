import json
import requests

from app.helper.alerts_manager import AlertsManager
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler

CONFIGRATIONS = Configrations()
ALERTSMANAGER = AlertsManager()

@error_handler
def login(email, password) -> str:
  data = {
    "email": email,
    "password": password
  }

  response = requests.get(
    CONFIGRATIONS.get_backend_endpoint() + "/login",
    params=data,
    timeout=5
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    return response.get("data")
  else:
    message = response.get("error")
    ALERTSMANAGER.error(
      message=message if message else "Something went wrong while checking user info",
    )
