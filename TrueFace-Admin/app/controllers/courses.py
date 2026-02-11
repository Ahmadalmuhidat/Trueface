import json
import requests

from app.interfaces.course import Course
from app.config.configurations import Configurations
from app.utils.error_handler import error_handler
from app.utils.alerts_manager import AlertsManager
from app.utils.session_manager import get_session

class CoursesController:
  def __init__(self):
    self._session = get_session()
    self._configurations = Configurations()
    self._alerts_manager = AlertsManager()

  @error_handler
  def fetch_courses(self) -> list:
    try:
      response = self._session.get(self._configurations.get_backend_endpoint() + "/courses/get_all")
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        return response_data.get("data")
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while getting the courses")
        return []

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return []
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return []

  @error_handler
  def fetch_courses(self) -> list:
    try:
      response = self._session.get(self._configurations.get_backend_endpoint() + "/courses/get_all")
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        return response_data.get("data")
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while getting the courses")
        return []

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return []
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return []

  @error_handler
  def update_course(self, course_object: Course) -> bool:
    try:
      data = {
        "course_id": course_object.id,
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

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/courses/update",
        data=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        self._alerts_manager.success("Course has been updated")
        return True
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while updating the courses")
        return False

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False

  @error_handler
  def add_course(self, course_object: Course) -> bool:
    try:
      data = {
        "course_id": course_object.id.lower(),
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

      response = self._session.post(
        self._configurations.get_backend_endpoint() + "/courses/insert",
        data=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        self._alerts_manager.success("New course has been added")
        return True
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while inserting the course")
        return False

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return False
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return False

  @error_handler
  def remove_course(self, course_object: Course) -> bool:
    confirmation = self._alerts_manager.options("Are you sure you want to delete the course")
    if confirmation:
      try:
        data = {
          "course_id": course_object.id
        }
        
        response = self._session.post(
          self._configurations.get_backend_endpoint() + "/courses/remove",
          data=data
        )
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("status_code") == 200:
          if response_data.get("data"):
            self._alerts_manager.success("Course has been deleted")
            return True
        else:
          message = response_data.get("error")
          self._alerts_manager.error(message if message else "Something went wrong while removing the course")
          return False

      except requests.exceptions.RequestException as e:
        self._alerts_manager.error(f"Network error: {str(e)}")
        return False
      except json.JSONDecodeError as e:
        self._alerts_manager.error(f"Invalid response format: {str(e)}")
        return False

  @error_handler
  def fetch_lectures_by_course(self, course_object: Course) -> list:
    try:
      data = {
        "course_id": course_object.id
      }
      
      response = self._session.get(
        self._configurations.get_backend_endpoint() + "/courses/get_lectures",
        params=data
      )
      response.raise_for_status()
      response_data = response.json()

      if response_data.get("status_code") == 200:
        return response_data.get("data")
      else:
        message = response_data.get("error")
        self._alerts_manager.error(message if message else "Something went wrong while getting the lectures")
        return []

    except requests.exceptions.RequestException as e:
      self._alerts_manager.error(f"Network error: {str(e)}")
      return []
    except json.JSONDecodeError as e:
      self._alerts_manager.error(f"Invalid response format: {str(e)}")
      return []
