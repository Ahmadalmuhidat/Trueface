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
			response = self._session.get(self._configurations.get_backend_endpoint() + "/students/get_all")
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				return response_data.get("data")
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while getting the students")
			return []

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
				"student_id": student_object.student_id.lower(),
				"first_name": student_object.first_name,
				"middle_name": student_object.middle_name,
				"last_name": student_object.last_name,
				"gender": student_object.gender.lower(),
				"face_encode": student_object.get_face_encode()
			}

			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/students/insert",
				data=data
			)
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				return response_data.get("data")
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while inserting the student")
				return False
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
				data = {
					"student_id": student_object.student_id
				}
		
				response = self._session.post(
					self._configurations.get_backend_endpoint() + "/students/remove", 
					data=data
				)
				response.raise_for_status()
				response_data = response.json()

				if response_data.get("status_code") == 200:
					if response_data.get("data"):
						self._alerts_manager.success("Student has been removed successfully")
						return True
				else:
					message = response_data.get("error")
					self._alerts_manager.error(message if message else "Something went wrong while removing the student")
					return False
			except requests.exceptions.RequestException as e:
				self._alerts_manager.error(f"Network error: {str(e)}")
				return False
			except json.JSONDecodeError as e:
				self._alerts_manager.error(f"Invalid response format: {str(e)}")
				return False

	@error_handler
	def add_student_to_lecture(self, relation_id: str, student_object: Student,  lecture: Lecture) -> bool:
		try:
			data = {
				"relation_id": relation_id,
				"student_id": student_object.student_id,
				"lecture_id": lecture.lecture_id,
				"day": lecture.day
			}
		
			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/students/add_lecture",
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
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False

	@error_handler
	def remove_student_from_lecture(self, student_object: Student, lecture: Lecture) -> bool:
		try:
			data = {
				"student_id": student_object.student_id,
				"lecture_id": lecture.lecture_id,
				"day": lecture.day
			}
		
			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/students/remove_lecture",
				data=data
			)
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				self._alerts_manager.success("Lecture has been removed successfully")
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
	def fetch_lectures_by_student(self, student_object: Student) -> list:
		try:
			data = {
				"student_id": student_object.student_id
			}

			response = self._session.get(
				self._configurations.get_backend_endpoint() + "/students/get_lectures", 
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

	@error_handler
	def update_student(self, student_object: Student) -> bool:
		try:
			data = {
				"student_id": student_object.student_id,
				"first_name": student_object.first_name,
				"middle_name": student_object.middle_name,
				"last_name": student_object.last_name,
				"gender": student_object.gender.lower(),
				"face_encode": student_object.get_face_encode()
			}
		
			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/students/update",
				data=data
			)
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				self._alerts_manager.success("Student has been updated successfully")
				return True
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while updating the student")
				return False
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False