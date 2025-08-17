import sys
import os
import json
import requests

from CTkMessagebox import CTkMessagebox
from app.models.user import User
from app.config.context import Context

def get_users() -> list:
	try:
		data_manager = Context()
		response = requests.get(data_manager.get_config().get_base_url() + "/get_users", timeout=20).content
		response = json.loads(response.decode('utf-8'))
		data_manager = Context()

		if response.get("status_code") == 200:
			data_manager.set_users(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while getting the users",
				icon = icon
			)

	except Exception as e: 
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)

def add_user(user_object: User) -> None:
	try:
		data = {
			"user_id": user_object.get_user_id(),
			"name": user_object.get_name(),
			"email": user_object.get_email(),
			"role": user_object.get_role()
		}
		data_manager = Context()
		response = requests.post(
			data_manager.get_config().get_base_url() + "/insert_user",
			data = data,
			timeout=20
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

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_user(user_id: str, refresh_table_function) -> None:
	try:
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
				"user_id": user_id,
			}
			data_manager = Context()
			response = requests.post(
				data_manager.get_config().get_base_url() + "/remove_user",
				data = data,
			  timeout=20
			).content
			response = json.loads(response.decode('utf-8'))

			if response.get("status_code") == 200:
				title="Success"
				message="User has been removed"
				icon="check"
				CTkMessagebox(title=title, message=message,icon=icon)
				refresh_table_function()
			else:
				title = "Error"
				message = response.get("error")
				icon = "cancel"
				CTkMessagebox(
					title = title,
					message = message if message else "Something went wrong while removing the user",
					icon = icon
				)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def search_user(user_id: str) -> list:
	try:
		data = {
			"user_id": user_id
		}
		data_manager = Context()
		response = requests.get(
			data_manager.get_config().get_base_url() + "/search_user",
			params = data,
			timeout=20
		).content
		response = json.loads(response.decode('utf-8'))
		data_manager = Context()

		if response.get("status_code") == 200:
			data_manager.set_users(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while searching in users",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

