import json
import requests

from CTkMessagebox import CTkMessagebox
from app.interfaces.lecture import Lecture
from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.error_handler import error_handler

CONTEXT = Context()
CONFIGRATIONS = Configrations()

@error_handler
def add_lecture(lecture_object: Lecture) -> None:
	data = {
		"class_id": lecture_object.lecture_id.lower(),
		"subject": lecture_object.subject_area,
		"catalog_nbr": lecture_object.catalog_nbr,
		"academic_career": lecture_object.academic_career,
		"course": lecture_object.Course,
		"offering_nbr": lecture_object.offering_nbr,
		"start_time": lecture_object.start_time,
		"end_time": lecture_object.end_time,
		"section": lecture_object.section,
		"component": lecture_object.component,
		"campus": lecture_object.campus,
		"instructor_id": lecture_object.instructor.instructor_id
	}

	response = requests.post(
		CONFIGRATIONS.get_backend_endpoint() + "/lectures/insert",
		data=data,
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
			title=title,
			message=message if message else "Something went wrong while inserting the lecture",
			icon=icon
		)

@error_handler
def remove_lecture(lecture_object: Lecture) -> None:
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
			"class_id": lecture_object.lecture_id
		}
		response = requests.post(
			CONFIGRATIONS.get_backend_endpoint() + "/lectures/remove",
			data = data,
			timeout=5
		).content
		response = json.loads(response.decode('utf-8'))

		if response.get("status_code") == 200:
			if response.get("data"):
				title = "Success"
				message = "Class has been deleted"
				icon = "check"
				CTkMessagebox(title=title, message=message,icon=icon)
		else:
			title = "Error"
			message = response.get("error")
			icon = "cancel"
			CTkMessagebox(
				title = title,
				message = message if message else "Something went wrong while removing the lecture",
				icon = icon
			)

@error_handler
def update_lecture(lecture_object: Lecture) -> None:
	data = {
		"lecture": lecture_object.lecture_id,
		"subject": lecture_object.subject_area,
		"catalog_nbr": lecture_object.catalog_nbr,
		"academic_career": lecture_object.academic_career,
		"course": CONTEXT.get_current_course().course_id,
		"offering_nbr": lecture_object.offering_nbr,
		"start_time": lecture_object.start_time,
		"end_time": lecture_object.end_time,
		"section": lecture_object.section,
		"component": lecture_object.component,
		"campus": lecture_object.campus,
		"instructor": lecture_object.instructor.instructor_id
	}

	response = requests.post(
		CONFIGRATIONS.get_backend_endpoint() + "/lectures/update",
		data=data,
		timeout=5
	).content
	response = json.loads(response.decode("utf-8"))

	if response.get("status_code") == 200:
		CTkMessagebox(title="Success", message="Lecture updated", icon="check")
	else:
		CTkMessagebox(
			title="Error",
			message=response.get("error") or "Something went wrong while updating the lecture",
			icon="cancel"
		)
