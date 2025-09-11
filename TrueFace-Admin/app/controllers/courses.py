import json
import requests

from app.interfaces.course import Course
from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler
from app.helper.alerts_manager import AlertsManager

CONTEXT = Context()
CONFIGRATIONS = Configrations()
ALERTSMANAGER = AlertsManager()

@error_handler
def get_courses() -> list:
  response = requests.get(CONFIGRATIONS.get_backend_endpoint() + "/courses/get_all", timeout=5).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    CONTEXT.set_courses(response.get("data"))
  else:
    message = response.get("error")
    ALERTSMANAGER.error(message if message else "Something went wrong while getting the courses",)

@error_handler
def update_course(course_object: Course) -> None:
  data = {
    "course_id": course_object.course_id.lower(),  # ID is fixed
    "title": course_object.title,
    "credit": course_object.credit,
    "maximum_units": course_object.maximum_units,
    "long_course_title": course_object.long_course_title,
    "offering_nbr": course_object.offering_nbr,
    "academic_group": course_object.academic_group,
    "subject_area": course_object.subject_area,
    "catalog_nbr": course_object.catalog_nbr,
    "campus": course_object.campus,
    "academic_organization": course_object.academic_organization,
    "component": course_object.component
  }

  response = requests.post(
    CONFIGRATIONS.get_backend_endpoint() + "/courses/update",
    data=data,
    timeout=5
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    message = "Course has been updated"
    ALERTSMANAGER.success(message)
  else:
    message = response.get("error")
    ALERTSMANAGER.error(message if message else "Something went wrong while updating the courses",)

@error_handler
def add_course(course_object: Course) -> None:
  data = {
    "course_id": course_object.course_id.lower(),
    "title": course_object.title,
    "credit": course_object.credit,
    "maximum_units": course_object.maximum_units,
    "long_course_title": course_object.long_course_title,
    "offering_nbr": course_object.offering_nbr,
    "academic_group": course_object.academic_group,
    "subject_area": course_object.subject_area,
    "catalog_nbr": course_object.catalog_nbr,
    "campus": course_object.campus,
    "academic_organization": course_object.academic_organization,
    "component": course_object.component
  }
  response = requests.post(
    CONFIGRATIONS.get_backend_endpoint() + "/courses/insert",
    data = data,
      timeout=5
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    return response.get("data")
  else:
    message = response.get("error")
    ALERTSMANAGER.error(message if message else "Something went wrong while inserting the course")

@error_handler
def remove_course(course_object: Course) -> None:
  conformation = ALERTSMANAGER.options("Are you sure you want to delete the course")
  if conformation:
    data = {
      "course_id": course_object.course_id
    }
    response = requests.post(
      CONFIGRATIONS.get_backend_endpoint() + "/courses/remove",
      data = data,
      timeout=5
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      if response.get("data"):
        message = "Course has been deleted"
        ALERTSMANAGER.success(message)
    else:
      message = response.get("error")
      ALERTSMANAGER.error(message if message else "Something went wrong while removing the course")

@error_handler
def get_lectures_by_course(course_object: Course) -> list:
  data = {
    "course_id": course_object.course_id
  }
  response = requests.get(
    CONFIGRATIONS.get_backend_endpoint() + "/courses/get_lectures",
    params=data,
    timeout=5
  ).content
  response = json.loads(response.decode('utf-8'))

  if response.get("status_code") == 200:
    return response.get("data")
  else:
    message = response.get("error")
    ALERTSMANAGER.error(message if message else "Something went wrong while getting the lectures")