import json
import requests

from app.helper.alerts_manager import AlertsManager
from app.interfaces.user import User
from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler

CONTEXT = Context()
CONFIGRATIONS = Configrations()
ALERTSMANAGER = AlertsManager()

@error_handler
def update_user(user_object: User) -> None:
	data = {
		"user_id": user_object.user_id.lower(),
		"name": user_object.name,
		"email": user_object.email,
		"role": user_object.role.lower()
	}

	response = requests.post(
		CONFIGRATIONS.get_backend_endpoint() + "/users/update",
		data=data,
		timeout=5
	).content
	response = json.loads(response.decode('utf-8'))

	if response.get("status_code") == 200:
		ALERTSMANAGER.success("User has been updated successfully")
	else:
		message = response.get("error")
		ALERTSMANAGER.error(message if message else "Something went wrong while updating the user")

@error_handler
def fetch_users() -> list:
	response = requests.get(CONFIGRATIONS.get_backend_endpoint() + "/users/get_all", timeout=5).content
	response = json.loads(response.decode('utf-8'))

	if response.get("status_code") == 200:
		CONTEXT.set_users(response.get("data"))
	else:
		message = response.get("error")
		ALERTSMANAGER.error(message if message else "Something went wrong while getting the users")

@error_handler
def add_user(user_object: User) -> None:
	data = {
		"user_id": user_object.user_id.lower(),
		"name": user_object.name,
		"email": user_object.email,
		"role": user_object.role.lower()
	}
	response = requests.post(
		CONFIGRATIONS.get_backend_endpoint() + "/users/insert",
		data = data,
		timeout=5
	).content
	response = json.loads(response.decode('utf-8'))

	if response.get("status_code") == 200:
		ALERTSMANAGER.success("New user has been added")
	else:
		message = response.get("error")
		ALERTSMANAGER.error(message if message else "Something went wrong while inserting the user")

@error_handler
def remove_user(user_object: User) -> None:
	conformation = ALERTSMANAGER.options("Are you sure you want to delete the user")
	if conformation:
		data = {
			"user_id": user_object.user_id,
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/users/remove",
			data = data,
			timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			ALERTSMANAGER.success("User has been removed")
		else:
			message = response.get("error")
			ALERTSMANAGER.error(message if message else "Something went wrong while removing the user")