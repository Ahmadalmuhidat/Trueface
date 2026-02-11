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
				"user_id": user_object.user_id.lower(),
				"name": user_object.name,
				"email": user_object.email,
				"role": user_object.role.lower()
			}

			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/users/update",
				data=data
			)
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				self._alerts_manager.success("User has been updated")
				return True
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while updating the user")
			return False

		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False

	@error_handler
	def fetch_users(self) -> list:
		try:
			response = self._session.get(self._configurations.get_backend_endpoint() + "/users/get_all")
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				return response_data.get("data")
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while getting the users")
				return []

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
				"user_id": user_object.user_id.lower(),
				"name": user_object.name,
				"email": user_object.email,
				"role": user_object.role.lower()
			}

			response = self._session.post(
				self._configurations.get_backend_endpoint() + "/users/insert",
				data=data
			)
			response.raise_for_status()
			response_data = response.json()

			if response_data.get("status_code") == 200:
				self._alerts_manager.success("New user has been added")
				return True
			else:
				message = response_data.get("error")
				self._alerts_manager.error(message if message else "Something went wrong while inserting the user")
				return False
		except requests.exceptions.RequestException as e:
			self._alerts_manager.error(f"Network error: {str(e)}")
			return False
		except json.JSONDecodeError as e:
			self._alerts_manager.error(f"Invalid response format: {str(e)}")
			return False

	@error_handler
	def remove_user(self, user_object: User) -> bool:
		confirmation = self._alerts_manager.options("Are you sure you want to delete the user")
		if confirmation:
			try:
				data = {
					"user_id": user_object.user_id,
				}	
				response = self._session.post(
					self._configurations.get_backend_endpoint() + "/users/remove",
					data=data
				)
				response.raise_for_status()
				response_data = response.json()

				if response_data.get("status_code") == 200:
					self._alerts_manager.success("User has been removed")
					return True
				else:
					message = response_data.get("error")
					self._alerts_manager.error(message if message else "Something went wrong while removing the user")
					return False
			except requests.exceptions.RequestException as e:
				self._alerts_manager.error(f"Network error: {str(e)}")
				return False
			except json.JSONDecodeError as e:
				self._alerts_manager.error(f"Invalid response format: {str(e)}")
				return False
