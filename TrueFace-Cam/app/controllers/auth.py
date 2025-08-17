import requests
import json

from CTkMessagebox import CTkMessagebox
from app.core.logger import Logger

LOGGER = Logger()

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
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while checking user info",
        icon = icon
      )

  except Exception as e: 
    LOGGER.log_exception(e)