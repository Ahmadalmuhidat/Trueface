import requests
import json

from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

LOGGER = Logger()
ALERTSMANAGR = AlertsManager()
CONTEXT = Context()
CONFIGRATIONS = Configrations()

@error_handler
def get_lectures_by_teacher():
  data = {
    "current_teacher": CONTEXT.get_jwt_token()
  }
  response = requests.get(
    CONFIGRATIONS.get_backend_endpoint() + "/lectures/get_by_teacher",
    params = data
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    CONTEXT.set_lectures(response.get("data"))
  else:
    message = response.get("error")
    ALERTSMANAGR.error(message if message else "Something went wrong while getting the classes")
