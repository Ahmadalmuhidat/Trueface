import requests
import json

from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

ALERTSMANAGR = AlertsManager()

@error_handler
def login(email, password):
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
    message = response.get("error")
    ALERTSMANAGR.error(message if message else "Something went wrong while logging in")