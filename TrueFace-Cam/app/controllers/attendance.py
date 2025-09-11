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
def insert_attendance(student_id, student_name):
  data = {
    "student_id": student_id,
    "current_class": CONTEXT.get_current_lecture().class_id
  }
  response = requests.post(
    CONFIGRATIONS.get_backend_endpoint() + "/attendance/insert",
    data = data
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    ALERTSMANAGR.pop_window(
      title = "Attendance Recorded",
      message = "{} has been signed".format(student_name),
      icon = "check"
    )
  else:
    message = response.get("error")
    ALERTSMANAGR.error(message if message else "Something went wrong while inserting attendance")