import cv2
import face_recognition
import time
import winsound

from datetime import datetime
from threading import Lock, Thread
from app.config.context import Context
from app.interfaces.student import Student
from app.config.configrations import Configrations
from app.controllers.attendance import insert_attendance
from app.helper.logger import Logger

class FaceRecognitionModule():
	def __init__(self) -> None:
		# private
		self._context = Context()
		self._config = Configrations()
		self._logger = Logger()

		self._scan_lock = Lock()

		self._last_frame_time = 0
		self._frame_interval = 0.5

	def analyze_camera_stream(self, frame) -> bool:
		try:
			if not self._should_process_frame():
				return

			# frame = self._downscale_frame(frame)
			face_locations = self._detect_faces(frame)
			known_encodings = self._get_known_encodings()

			if face_locations and known_encodings:
				cam_face_encodings = self._encode_faces(frame, face_locations)

				if cam_face_encodings:
					matches = self._compare_faces(known_encodings, cam_face_encodings[0])
					self._process_matches(matches)

		except Exception as e:
			self._logger.log_exception(e)

	def _should_process_frame(self) -> bool:
		current_time = time.time()
		if current_time - self._last_frame_time < self._frame_interval:
			return False
		self._last_frame_time = current_time
		return True

	def _downscale_frame(self, frame):
		return cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	def _detect_faces(self, frame):
		model = "hog" if self._config.get_processing_mode() == "CPU" else "gnn"
		return face_recognition.face_locations(frame, model=model)

	def _get_known_encodings(self):
		return [student.get_face_encode() for student in self._context.get_students()]

	def _encode_faces(self, frame, face_locations):
		return face_recognition.face_encodings(frame, face_locations)

	def _compare_faces(self, known_encodings, cam_face_encodings):
		return face_recognition.compare_faces(known_encodings, cam_face_encodings, tolerance=0.5)

	def _process_matches(self, matches):
		for i, match in enumerate(matches):
			if match:
				with self._scan_lock:
					student = self._context.get_students()[i]
					if not student.is_attended():
						self._record_attendance(student)
						Thread(target=winsound.Beep, args=(2500, 500)).start()

	def _record_attendance(self, student: Student):
		self._config.frame_processing_executor.submit(
			insert_attendance,
			student.student_id,
			f"{student.first_name} {student.last_name}"
		)
		student.confirm_attendance()
