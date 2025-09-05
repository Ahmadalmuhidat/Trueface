import cv2
import face_recognition
import time
import winsound

from threading import Lock, Thread
from app.config.context import Context
from app.interfaces.student import Student
from app.controllers.attendance import insert_attendance
from app.helper.error_handler import error_handler
from app.interfaces.recognizer import Recognizer

class FaceRecognitionModule(Recognizer):
	def __init__(self) -> None:
		super().__init__()

		from app.config.configrations import Configrations

		# private
		self._context = Context()
		self._config = Configrations()

		self._scan_lock = Lock()

	@error_handler
	def analyze_camera_stream(self, frame) -> bool:
		face_locations = self._detect_faces(frame)
		known_encodings = self._get_known_encodings()

		if face_locations and known_encodings:
			cam_face_encodings = self._encode_faces(frame, face_locations)

			if cam_face_encodings:
				matches = self._compare_faces(known_encodings, cam_face_encodings[0])
				self._process_matches(matches)

	@error_handler
	def _detect_faces(self, frame):
		model = "hog" if self._config.get_processing_mode() == "CPU" else "gnn"
		return face_recognition.face_locations(frame, model=model)

	def _get_known_encodings(self):
		return [student.get_face_encode() for student in self._context.get_students()]

	@error_handler
	def _encode_faces(self, frame, face_locations):
		return face_recognition.face_encodings(frame, face_locations)

	@error_handler
	def _compare_faces(self, known_encodings, cam_face_encodings):
		return face_recognition.compare_faces(known_encodings, cam_face_encodings, tolerance=0.5)

	@error_handler
	def _process_matches(self, matches):
		for i, match in enumerate(matches):
			if match:
				with self._scan_lock:
					student = self._context.get_students()[i]
					if not student.is_attended():
						self._record_attendance(student)
						Thread(target=winsound.Beep, args=(2500, 500)).start()

	@error_handler
	def _record_attendance(self, student: Student):
		self._config.frame_processing_executor.submit(
			insert_attendance,
			student.student_id,
			f"{student.first_name} {student.last_name}"
		)
		student.confirm_attendance()
