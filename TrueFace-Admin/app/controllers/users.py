import json
import requests

from app.utils.alerts_manager import AlertsManager
from app.interfaces.user import User
from app.config.configurations import Configurations
from app.utils.error_handler import error_handler
from app.utils.session_manager import get_session

class UsersController:
	def __init__(self):
		self._session = get_session()
		self._configurations = Configurations()
		self._alerts_manager = AlertsManager()

	@error_handler
	def update_user(self, user_object: User) -> bool:
		try:
			data = {
				"id": user_object.user_id.lower(),
				"name": user_object.name,
				"email": user_object.email,
				"role": user_object.role.lower()
			}

			response = self._session.put(
				f"{self._configurations.get_backend_endpoint()}/users/{user_object.user_id}/",
				json=data
			)
			response.raise_for_status()
			self._alerts_manager.success("User has been updated")
			return True

		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False

	@error_handler
	def fetch_users(self) -> list:
		try:
			response = self._session.get(self._configurations.get_backend_endpoint() + "/users/")
			response.raise_for_status()
			data = response.json()

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
	def add_user(self, user_object: User) -> bool:
		try:
			data = {
				"id": user_object.user_id.lower(),
				"name": user_object.name,
				"email": user_object.email,
				"role": user_object.role.lower()
			}

			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/users/",
				json=data
			)
			response.raise_for_status()
			self._alerts_manager.success("New user has been added")
			return True
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False

	@error_handler
	def remove_user(self, user_object: User) -> bool:
		confirmation = self._alerts_manager.options("Are you sure you want to delete the user")
		if confirmation:
			try:
				response = self._session.delete(
					f"{self._configurations.get_backend_endpoint()}/users/{user_object.user_id}/"
				)
				response.raise_for_status()
				self._alerts_manager.success("User has been removed")
				return True
			except requests.exceptions.RequestException as e:
				self._alerts_manager.error(f"Network error: {str(e)}")
				return False
