import json
import requests

from CTkMessagebox import CTkMessagebox
from app.interfaces.user import User
from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler

CONTEXT = Context()
CONFIGRATIONS = Configrations()

@error_handler
def get_users() -> list:
	response = requests.get(CONFIGRATIONS.get_backend_endpoint() + "/users/get_all", timeout=5).content
	response = json.loads(response.decode('utf-8'))

	if response.get("status_code") == 200:
		CONTEXT.set_users(response.get("data"))
	else:
		title = "Error"
		message = response.get("error")
		icon = "cancel"
		CTkMessagebox(
			title = title,
			message = message if message else "Something went wrong while getting the users",
			icon = icon
		)

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
		title="Success"
		message="New user has been added"
		icon="check"
		CTkMessagebox(
			title = title,
			message = message,
			icon = icon
		)
	else:
		title = "Error"
		message = response.get("error")
		icon = "cancel"
		CTkMessagebox(
			title = title,
			message = message if message else "Something went wrong while inserting the user",
			icon = icon
		)

@error_handler
def remove_user(user_object: User) -> None:
	title = "Conformation"
	message = "Are you sure you want to delete the user"
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
			"user_id": user_object.user_id,
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/users/remove",
			data = data,
			timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			title="Success"
			message="User has been removed"
			icon="check"
			CTkMessagebox(title=title, message=message,icon=icon)
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while removing the user",
				icon = icon
			)