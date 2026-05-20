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
        "id": lecture_object.lecture_id.lower(),
        "subject_area": lecture_object.subject_area,
        "catalog_nbr": lecture_object.catalog_nbr,
        "academic_career": lecture_object.academic_career,
        "course": lecture_object.course,
        "offering_nbr": lecture_object.offering_nbr,
        "start_time": lecture_object.start_time,
        "end_time": lecture_object.end_time,
        "section": lecture_object.section,
        "component": lecture_object.component,
        "campus": lecture_object.campus,
        "instructor": lecture_object.instructor.id
      }

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/lectures/",
        json=data
      )
      response.raise_for_status()
      self._alerts_manager.success("New lecture has been added")
      return True

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False

  @error_handler
  def remove_lecture(self, lecture_object: Lecture) -> bool:
    confirmation = self._alerts_manager.options("Are you sure you want to delete the lecture")
    if confirmation:
      try:
        response = self._session.delete(
          f"{self._configurations.get_backend_endpoint()}/lectures/{lecture_object.lecture_id}/"
        )
        response.raise_for_status()
        self._alerts_manager.success("Lecture has been deleted")
        return True

      except requests.exceptions.RequestException as e:
        self._alerts_manager.error(f"Network error: {str(e)}")
        return False

  @error_handler
  def update_lecture(self, lecture_object: Lecture) -> bool:
    try:
      data = {
        "id": lecture_object.lecture_id,
        "subject_area": lecture_object.subject_area,
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

      response = self._session.put(
        f"{self._configurations.get_backend_endpoint()}/lectures/{lecture_object.lecture_id}/",
        json=data
      )
      response.raise_for_status()
      self._alerts_manager.success("Lecture has been updated")
      return True

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
