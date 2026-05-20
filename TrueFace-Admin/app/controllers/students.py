import json
import requests

from app.utils.alerts_manager import AlertsManager
from app.interfaces.student import Student
from app.interfaces.lecture import Lecture
from app.config.configurations import Configurations
from app.utils.error_handler import error_handler
from app.utils.session_manager import get_session

class StudentsController:
	def __init__(self):
		self._session = get_session()
		self._configurations = Configurations()
		self._alerts_manager = AlertsManager()
	
	@error_handler
	def fetch_students(self) -> list:
		try:
			response = self._session.get(self._configurations.get_backend_endpoint() + "/students/")
			response.raise_for_status()
			data = response.json()

			# Standard DRF response might be a list or a paginated dict with 'results'
			if isinstance(data, dict) and "results" in data:
				return data["results"]
			return data

		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return []
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return []

	@error_handler
	def add_student(self, student_object: Student) -> bool:
		try:
			data = {
				"id": student_object.student_id.lower(),
				"first_name": student_object.first_name,
				"middle_name": student_object.middle_name,
				"last_name": student_object.last_name,
				"gender": student_object.gender.lower(),
				"face_id": student_object.get_face_encode()
			}

			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/students/",
				json=data
			)
			response.raise_for_status()
			return True
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False

	@error_handler
	def remove_student(self, student_object: Student) -> bool:
		confirmation = self._alerts_manager.options("Are you sure you want to delete the student")
		if confirmation:
			try:
				response = self._session.delete(
					f"{self._configurations.get_backend_endpoint()}/students/{student_object.student_id}/"
				)
				response.raise_for_status()
				self._alerts_manager.success("Student has been removed successfully")
				return True
			except requests.exceptions.RequestException as e:
				self._alerts_manager.error(f"Network error: {str(e)}")
				return False

	@error_handler
	def add_student_to_lecture(self, relation_id: str, student_object: Student,  lecture: Lecture) -> bool:
		try:
			data = {
				"relation_id": relation_id,
				"lecture_id": lecture.lecture_id,
				"day": lecture.day
			}
		
			response = self._session.post(
				f"{self._configurations.get_backend_endpoint()}/students/{student_object.student_id}/add_lecture/",
				json=data
			)
			response.raise_for_status()
			self._alerts_manager.success("New lecture has been added")
			return True
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False

	@error_handler
	def remove_student_from_lecture(self, student_object: Student, lecture: Lecture) -> bool:
		try:
			data = {
				"lecture_id": lecture.lecture_id,
				"day": lecture.day
			}
		
			response = self._session.delete(
				f"{self._configurations.get_backend_endpoint()}/students/{student_object.student_id}/remove_lecture/",
				json=data
			)
			response.raise_for_status()
			self._alerts_manager.success("Lecture has been removed successfully")
			return True
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False

	@error_handler
	def fetch_lectures_by_student(self, student_object: Student) -> list:
		try:
			response = self._session.get(
				f"{self._configurations.get_backend_endpoint()}/students/{student_object.student_id}/lectures/"
			)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return []

	@error_handler
	def update_student(self, student_object: Student) -> bool:
		try:
			data = {
				"id": student_object.student_id,
				"first_name": student_object.first_name,
				"middle_name": student_object.middle_name,
				"last_name": student_object.last_name,
				"gender": student_object.gender.lower(),
				"face_id": student_object.get_face_encode()
			}
		
			response = self._session.put(
				f"{self._configurations.get_backend_endpoint()}/students/{student_object.student_id}/",
				json=data
			)
			response.raise_for_status()
			self._alerts_manager.success("Student has been updated successfully")
			return True
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False