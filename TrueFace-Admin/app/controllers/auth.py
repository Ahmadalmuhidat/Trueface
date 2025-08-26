import json
import requests

from CTkMessagebox import CTkMessagebox
from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler

CONFIGRATIONS = Configrations()

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
    title = "Error"
    message = response.get("error")
    icon = "cancel"
    CTkMessagebox(
      title=title,
      message=message if message else "Something went wrong while checking user info",
      icon=icon
    )

