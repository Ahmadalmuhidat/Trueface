import sys
import os
import json
import requests

from CTkMessagebox import CTkMessagebox
from app.models.student import Student
from app.config.context import Context

def get_students() -> list:
	try:
		data_manager = Context()
		response = requests.get(data_manager.get_config().get_base_url() + "/get_all_students").content
		response = json.loads(response.decode('utf-8'))
		data_manager = Context()

		if response.get("status_code") == 200:
			data_manager.set_students(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while getting the students",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def add_student(student_object: Student) -> None:
	try:
		data = {
			"student_id": student_object.get_student_id(),
			"first_name": student_object.get_first_name(),
			"middle_name": student_object.get_middle_name(),
			"last_name": student_object.get_last_name(),
			"gender": student_object.get_gender(),
			"face_encode": student_object.get_face_encode()
		}
		data_manager = Context()

		response = requests.post(
			data_manager.get_config().get_base_url() + "/insert_student",
			data = data,
			timeout=20
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			return response.get("data")
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while inserting the student",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_student(student_id: str, refresh_table_function) -> None:
	try:
		title = "Conformation"
		message = "Are you sure you want to delete the student"
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
				"student_id": student_id
			}
			data_manager = Context()
			response = requests.post(
				data_manager.get_config().get_base_url() + "/remove_student", 
				data = data,
			  timeout=20
			).content
			response = json.loads(response.decode('utf-8'))

			if response.get("status_code") == 200:
				if response.get("data"):
					title = "Relation has been deleted"
					message = "Class has been removed successfully"
					icon = "check"
					CTkMessagebox(title=title, message=message,icon=icon)
					refresh_table_function()
			else:
				title = "Error"
				message = response.get("error")
				icon = "cancel"
				CTkMessagebox(
					title = title,
					message = message if message else "Something went wrong while removing the student",
					icon = icon
				)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def search_student(student_id: str) -> list:
	try:
		data = {
			"student_id": str(student_id)
		}
		data_manager = Context()
		response = requests.get(
			data_manager.get_config().get_base_url() + "/search_student",
			params = data,
			timeout=20
		).content
		response = json.loads(response.decode('utf-8'))
		data_manager = Context()

		if response.get("status_code") == 200:
			data_manager.set_students(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while searching in students",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass
