import requests
import json

from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager

LOGGER = Logger()
ALERTS_MANAGR = AlertsManager()
CONTEXT = Context()
CONFIGRATIONS = Configrations()

def search_attendance(student_id):
  try:
    return []

  except Exception as e:
    LOGGER.log_exception(e)
    pass

def insert_attendance(student_id, student_name):
  try:
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
      ALERTS_MANAGR.pop_window(
        title = "Attendance Recorded",
        message = "{} has been signed".format(student_name),
        icon = "check"
      )
    else:
      ALERTS_MANAGR.pop_window(
        title = "Error",
        message = response.get("error") if response.get("error") else "Something went wrong while inserting attendance",
        icon = "cancel"
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass
