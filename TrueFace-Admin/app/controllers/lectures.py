import json
import requests

from app.utils.alerts_manager import AlertsManager
from app.interfaces.lecture import Lecture
from app.config.configurations import Configurations
from app.utils.error_handler import error_handler
from app.utils.session_manager import get_session
from app.config.context import Context

class LecturesController:
  def __init__(self):
    self._session = get_session()
    self._configurations = Configurations()
    self._alerts_manager = AlertsManager()
    self._context = Context()

  @error_handler
  def get_all_lectures(self) -> [Lecture]:
    lectures = []
    for course in self._context.get_courses():
      course_lectures = course.get_lectures()
      lectures.extend(course_lectures)
    return lectures

  @error_handler
  def add_lecture(self, lecture_object: Lecture) -> bool:
    try:
      data = {
        "lecture_id": lecture_object.lecture_id.lower(),
        "subject": lecture_object.subject_area,
        "catalog_nbr": lecture_object.catalog_nbr,
        "academic_career": lecture_object.academic_career,
        "course": lecture_object.course,
        "offering_nbr": lecture_object.offering_nbr,
        "start_time": lecture_object.start_time,
        "end_time": lecture_object.end_time,
        "section": lecture_object.section,
        "component": lecture_object.component,
        "campus": lecture_object.campus,
        "instructor_id": lecture_object.instructor.id
      }

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/lectures/insert",
        data=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        self._alerts_manager.success("New lecture has been added")
        return True
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while inserting the lecture")
        return False

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")

  @error_handler
  def remove_lecture(self, lecture_object: Lecture) -> bool:
    confirmation = self._alerts_manager.options("Are you sure you want to delete the lecture")
    if confirmation:
      try:
        data = {
          "lecture_id": lecture_object.lecture_id
        }

        response = self._session.post(
          self._configurations.get_backend_endpoint() + "/lectures/remove",
          data=data
        )
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("status_code") == 200:
          if response_data.get("data"):
            self._alerts_manager.success("Lecture has been deleted")
            return True
        else:
          message = response_data.get("error")
          self._alerts_manager.error(message if message else "Something went wrong while removing the lecture")
          return False

      except requests.exceptions.RequestException as e:
        self._alerts_manager.error(f"Network error: {str(e)}")
        return False
      except json.JSONDecodeError as e:
        self._alerts_manager.error(f"Invalid response format: {str(e)}")
        return False

  @error_handler
  def update_lecture(self, lecture_object: Lecture) -> bool:
    try:
      data = {
        "lecture": lecture_object.lecture_id,
        "subject": lecture_object.subject_area,
        "catalog_nbr": lecture_object.catalog_nbr,
        "academic_career": lecture_object.academic_career,
        "course": self._context.get_current_course().id,
        "offering_nbr": lecture_object.offering_nbr,
        "start_time": lecture_object.start_time,
        "end_time": lecture_object.end_time,
        "section": lecture_object.section,
        "component": lecture_object.component,
        "campus": lecture_object.campus,
        "instructor": lecture_object.instructor.id
      }

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/lectures/update",
        data=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        self._alerts_manager.success("Lecture has been updated")
        return True
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while updating the lecture")
        return False

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False
