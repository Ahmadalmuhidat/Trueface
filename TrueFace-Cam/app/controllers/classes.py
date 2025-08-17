import requests
import json

from CTkMessagebox import CTkMessagebox
from app.config.context import Context
from app.core.logger import Logger

LOGGER = Logger()

def get_classes_by_teacher():
  try:
    context = Context()
    data = {
      "current_teacher": context.get_jwt_token()
    }
    response = requests.get(
      context.get_config().get_backend_endpoint() + "/get_classes_by_teacher",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      context.set_classes(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the classes",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass