import requests
import json

from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

ALERTSMANAGR = AlertsManager()
CONTEXT = Context()
CONFIGRATIONS = Configrations()

@error_handler
def get_students_by_lecture():
  if not CONTEXT.get_current_lecture():
    ALERTSMANAGR.error(message="Please select a class first.")
    return

  data = {
    "current_class": CONTEXT.get_current_lecture().class_id
  }
  response = requests.get(
    CONFIGRATIONS.get_backend_endpoint() + "/lectures/get_students",
    params = data
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    CONTEXT.set_students(response.get("data"))
  else:
    message = response.get("error")
    ALERTSMANAGR.error(message = message if message else "Something went wrong while getting the students")