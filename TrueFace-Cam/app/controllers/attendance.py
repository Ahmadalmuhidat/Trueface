import requests
import json

from CTkMessagebox import CTkMessagebox
from app.config.context import Context
from app.core.logger import Logger

LOGGER = Logger()

def get_attendance_by_class():
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
      context.get_config().get_backend_endpoint() + "/get_attendance_by_class",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      context.set_attendance(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the attendance",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass

def search_attendance(student_id):
  try:
    context = Context()
    data = {
      "student_id": student_id,
    }
    response = requests.get(
      context.get_config().get_backend_endpoint() + "/search_attendance",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      context.set_attendance(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while searching in the attendance",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass

def check_attendance(student_id):
  try:
    context = Context()
    data = {
      "student_id": student_id,
      "current_class": context.get_current_class().class_id
    }
    response = requests.get(
      context.get_config().get_backend_endpoint() + "/check_attendance",
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
        message = message if message else "Something went wrong while checking student attendance",
        icon = icon
      )

  except Exception as e:
    LOGGER.log_exception(e)
    pass

def insert_attendance(student_id, student_name):
  try:
    if not check_attendance(student_id):
      context = Context()
      data = {
        "student_id": student_id,
        "current_class": context.get_current_class().class_id
      }
      response = requests.post(
        context.get_config().get_backend_endpoint() + "/insert_attendance",
        data = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        CTkMessagebox(
          title = "Attendance Recorded",
          message = "{} has been signed".format(student_name),
          icon = "check"
        )
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while inserting attendance",
          icon = icon
        )

  except Exception as e:
    LOGGER.log_exception(e)
    pass
