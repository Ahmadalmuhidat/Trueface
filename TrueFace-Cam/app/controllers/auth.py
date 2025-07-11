import os
import sys
import requests
import json

from app.config.context import Context
from CTkMessagebox import CTkMessagebox

def login(email, password):
  try:
    database_manager = Context()
    data = {
      "email": email,
      "password": password
    }
    response = requests.get(
      "http://localhost:8000/admin/check_user",
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
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)