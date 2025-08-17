import sys
import os
import json
import requests

from CTkMessagebox import CTkMessagebox
from app.models.course import Course
from app.config.context import Context

def get_courses() -> list:
  try:
    data_manager = Context()
    response = requests.get(data_manager.get_config().get_base_url() + "/get_courses", timeout=20).content
    response = json.loads(response.decode('utf-8'))
    data_manager = Context()

    if response.get("status_code") == 200:
      data_manager.set_courses(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the courses",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass 

def add_course(course_object: Course) -> None:
  try:
    data = {
      "course_id": course_object.get_course_id(),
      "title": course_object.get_title(),
      "credit": course_object.get_credit(),
      "maximum_units": course_object.get_maximum_units(),
      "long_course_title": course_object.get_long_course_title(),
      "offering_nbr": course_object.get_offering_nbr(),
      "academic_group": course_object.get_academic_group(),
      "subject_area": course_object.get_subject_area(),
      "catalog_nbr": course_object.get_catalog_nbr(),
      "campus": course_object.get_campus(),
      "academic_organization": course_object.get_academic_organization(),
      "component": course_object.get_component()
    }
    data_manager = Context()
    response = requests.post(
      data_manager.get_config().get_base_url() + "/insert_course",
      data = data,
				timeout=20
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
        message = message if message else "Something went wrong while inserting the course",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass

def remove_course(course_id: str, refresh_table_function) -> None:
  try:
    title = "Conformation"
    message = "Are you sure you want to delete the course"
    icon = "question"
    conformation = CTkMessagebox(
      title = title,
      message = message,
      icon = icon,
      option_1 = "yes",
      option_2 = "cancel" 
    )

    if conformation.get() == "yes":
      data = {
        "course_id": course_id
      }
      data_manager = Context()
      response = requests.post(
        data_manager.get_config().get_base_url() + "/remove_course",
        data = data,
				timeout=20
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        if response.get("data"):
          title = "Success"
          message = "Course has been deleted"
          icon = "check"
          CTkMessagebox(title=title, message=message,icon=icon)
          refresh_table_function()
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while removing the course",
          icon = icon
        )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)

def search_course(course_id: str) -> list:
  try:
    data = {
      "course_id": course_id
    }
    data_manager = Context()
    response = requests.get(
      data_manager.get_config().get_base_url() + "/search_courses",
      params = data,
			timeout=20
    ).content
    response = json.loads(response.decode('utf-8'))
    data_manager = Context()

    if response.get("status_code") == 200:
      data_manager.set_courses(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while searching in courses",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass 
