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

def get_students_by_lecture():
  try:
    if not CONTEXT.get_current_lecture():
      ALERTS_MANAGR.pop_window(
        title="Error",
        message="Please select a class first.",
        icon="cancel"
      )
      return

    data = {
      "current_class": CONTEXT.get_current_lecture().class_id
    }
    response = requests.get(
      CONFIGRATIONS.get_backend_endpoint() + "lectures/get_students",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      CONTEXT.set_students(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      ALERTS_MANAGR.pop_window(
        title = title,
        message = message if message else "Something went wrong while getting the students",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass