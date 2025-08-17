import requests
import json

from app.config.context import Context
from CTkMessagebox import CTkMessagebox
from app.core.logger import Logger

LOGGER = Logger()

def get_students_by_class():
  try:
    context = Context()
    if not context.current_class:
      CTkMessagebox(
        title="Error",
        message="Please select a class first.",
        icon="cancel"
      )
      return

    data = {
      "current_class": context.get_current_class().class_id
    }
    response = requests.get(
      context.get_config().get_backend_endpoint() + "/get_students_by_class",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      context.set_students(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the students",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass