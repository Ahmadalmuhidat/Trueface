import requests
import json

from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager

LOGGER = Logger()
ALERTS_MANAGR = AlertsManager()

def login(email, password):
  try:
    data = {
      "email": email,
      "password": password
    }
    response = requests.get(
      "http://34.29.161.87:8000/admin/login",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      return response.get("data")
    else:
      ALERTS_MANAGR.pop_window(
        title = "Error",
        message = response.get("error") if response.get("error") else "Something went wrong while logging in",
        icon = "cancel"
      )

  except Exception as e: 
    LOGGER.log_exception(e)