import sys
import os
import json
import requests

from CTkMessagebox import CTkMessagebox
from app.interfaces.student import Student
from app.config.context import Context
from app.interfaces.lecture import Lecture
from app.config.configrations import Configrations

CONTEXT = Context()
CONFIGRATIONS = Configrations()

def get_students() -> list:
	try:
		response = requests.get(CONFIGRATIONS.get_backend_endpoint() + "/students/get_all").content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			CONTEXT.set_students(response.get("data"))
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
			"student_id": student_object.student_id,
			"first_name": student_object.first_name,
			"middle_name": student_object.middle_name,
			"last_name": student_object.last_name,
			"gender": student_object.gender,
			"face_encode": student_object.get_face_encode()
		}

		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/students/insert",
			data = data,
			timeout=5
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

def remove_student(student_object: Student) -> None:
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
			"student_id": student_object.student_id
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/students/remove", 
			data = data,
			timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			if response.get("data"):
				title = "Relation has been deleted"
				message = "Class has been removed successfully"
				icon = "check"
				CTkMessagebox(title=title, message=message,icon=icon)
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while removing the student",
				icon = icon
			)

def add_student_to_lecture(relation_id: str, student_object: Student,  lecture: Lecture, class_day: str) -> None:
	try:
		data = {
			"relation_id": relation_id,
			"student_id": student_object.student_id,
			"class_id": lecture.lecture_id,
			"day": class_day
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/students/add_lecture",
			data = data,
				timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			title="Success"
			message="New lecture has been added"
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
				message = message if message else "Something went wrong while inserting the lecture",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_student_from_all_lectures(student_object: Student) -> None:
	try:
		data = {
			"student_id": student_object.student_id
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/students/clear_lectures",
			data = data,
			timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			if response.get("data"):
				title = "Classes has been cleared"
				message = "Class has been cleared successfully"
				icon = "check"
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
				message = message if message else "Something went wrong while clearing the lectures",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_student_from_lecture(student: Student, lecture: Lecture) -> None:
	try:
		title = "Conformation"
		message = "Are you sure you want to delete the lecture"
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
				"student_id": student.student_id,
				"lecture_id": lecture.lecture_id,
				"day": lecture.day
			}
			response = requests.post(
				CONFIGRATIONS.get_backend_endpoint() + "/students/remove_lecture",
				data = data,
				timeout=5
			).content
			response = json.loads(response.decode('utf-8'))

			if response.get("status_code") == 200:
				if response.get("data"):
					title = "Class has been removed"
					message = "Class has been removed successfully"
					icon = "check"
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
					message = message if message else "Something went wrong while removing the lecture",
					icon = icon
				)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def get_lectures_by_student(student_object: Student) -> None:
	try:
		data = {
			"student_id": student_object.student_id
		}
		response = requests.get(
			CONFIGRATIONS.get_backend_endpoint() + "/students/get_lectures",
			params = data,
			timeout=5
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
				message = message if message else "Something went wrong while getting lectures for the student",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass