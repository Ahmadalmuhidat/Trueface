import sys
import os
import json
import requests

from CTkMessagebox import CTkMessagebox
from app.models.class_ import Class, RelationClass
from app.config.context import Context

def get_classes() -> list:
	try:
		data_manager = Context()
		response = requests.get(data_manager.get_config().get_base_url() + "/get_classes", timeout=20).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			data_manager.set_classes(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title=title,
				message=message if message else "Something went wrong while getting the classes",
				icon=icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def add_class(class_object: Class) -> None:
	try:
		data = {
			"class_id": class_object.get_class_id(),
			"subject": class_object.get_subject_area(),
			"catalog_nbr": class_object.get_catalog_nbr(),
			"academic_career": class_object.get_academic_career(),
			"course": class_object.get_course(),
			"offering_nbr": class_object.get_offering_nbr(),
			"start_time": class_object.get_start_time(),
			"end_time": class_object.get_end_time(),
			"section": class_object.get_section(),
			"component": class_object.get_component(),
			"campus": class_object.get_campus(),
			"instructor_id": class_object.get_instructor_id(),
			"instructor_type": class_object.get_instructor_type()
		}
		data_manager = Context()

		response = requests.post(
			data_manager.get_config().get_base_url() + "/insert_class",
			data=data,
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
				title=title,
				message=message if message else "Something went wrong while inserting the class",
				icon=icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_class(class_id: str, refresh_table_function) -> None:
	try:
		title = "Conformation"
		message = "Are you sure you want to delete the class"
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
				"class_id": class_id
			}
			data_manager = Context()
			response = requests.post(
				data_manager.get_config().get_base_url() + "/remove_class",
				data = data,
				timeout=20
			).content
			response = json.loads(response.decode('utf-8'))

			if response.get("status_code") == 200:
				if response.get("data"):
					title = "Success"
					message = "Class has been deleted"
					icon = "check"
					CTkMessagebox(title=title, message=message,icon=icon)
					refresh_table_function()
			else:
				title = "Error"
				message = response.get("error")
				icon = "cancel"
				CTkMessagebox(
					title = title,
					message = message if message else "Something went wrong while removing the class",
					icon = icon
				)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def search_class(class_id: str) -> list:
	try:
		data = {
			"class_id": class_id
		}
		data_manager = Context()
		response = requests.get(
			data_manager.get_config().get_base_url() + "/search_class",
			params = data,
				timeout=20
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			data_manager.set_classes(response.get("data"))
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while searching in classes",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def get_student_classes(student_id: str) -> None:
	try:
		data = {
			"student_id": student_id
		}
		data_manager = Context()
		response = requests.get(
			data_manager.get_config().get_base_url() + "/get_classes_student_relation",
			params = data,
				timeout=20
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			return [
				RelationClass(
					relation_id = data['Relation'],
					class_id = data['Class'],
					SubjectArea = data['SubjectArea'],
					StartTime = data['StartTime'],
					EndTime = data['EndTime'],
					day = data['Day']
				) for data in response.get("data")
			]
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while getting classes for the student",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_student_from_class(relation_id: str) -> None:
	try:
		title = "Conformation"
		message = "Are you sure you want to delete the class"
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
				"relation_id": relation_id
			}
			data_manager = Context()
			response = requests.post(
				data_manager.get_config().get_base_url() + "/remove_class_student_relation",
				data = data,
				timeout=20
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
					message = message if message else "Something went wrong while removing the class",
					icon = icon
				)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def remove_student_from_all_classes(student_id: str) -> None:
	try:
		data = {
			"student_id": student_id
		}
		data_manager = Context()
		response = requests.post(
			data_manager.get_config().get_base_url() + "/clear_class_student_relation",
			data = data,
			timeout=20
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
				message = message if message else "Something went wrong while clearing the classes",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def get_classes_for_selection() -> list:
	try:
		data_manager = Context()
		response = requests.get(
			data_manager.get_config().get_base_url() + "/get_classes_for_selection", timeout=20
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			return [
				Class(
					class_id = data['ID'],
					subject_area = data['SubjectArea'],
					start_time = data['StartTime'],
					end_time = data['EndTime'],
				) for data in response.get("data")
			]
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while getting classes",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass

def add_student_to_class(relation_id: str, student_id: str, class_id: str, class_day: str) -> None:
	try:
		data = {
			"relation_id": relation_id,
			"student_id": student_id,
			"class_id": class_id,
			"day": class_day
		}
		data_manager = Context()
		response = requests.post(
			data_manager.get_config().get_base_url() + "/insert_class_student_relation",
			data = data,
				timeout=20
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			title="Success"
			message="New class has been added"
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
				message = message if message else "Something went wrong while inserting the class",
				icon = icon
			)

	except Exception as e:
		ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
		FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
		print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
		print(ExceptionObject)
		pass
