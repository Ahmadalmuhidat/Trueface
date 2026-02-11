import cv2
import face_recognition
import time
import winsound
import numpy

from typing import List, Tuple
from threading import Lock, Thread
from app.config.context import Context
from app.interfaces.student import Student
from app.controllers.attendance import AttendanceController
from app.utils.error_handler import error_handler
from app.interfaces.recognizer import Recognizer

class FaceRecognitionModule(Recognizer):
	def __init__(self) -> None:
		super().__init__()
		from app.config.configurations import Configurations

		self.attendace_controller = AttendanceController()

		self._context = Context()
		self._config = Configurations()
		self._scan_lock = Lock()

		self._cached_encodings = None
		self._last_student_count = 0
		self._encoding_cache_valid = False

	@error_handler
	def process_camera_stream(self, frame: numpy.ndarray) -> None:
		face_locations = self._detect_faces(frame)
		known_encodings = self._get_known_encodings()

		if face_locations and known_encodings:
			cam_face_encodings = self._encode_faces(frame, face_locations)

			if cam_face_encodings:
				matches = self._compare_faces(known_encodings, cam_face_encodings[0])
				self._process_matches(matches)

	@error_handler
	def _detect_faces(self, frame: numpy.ndarray) -> List[Tuple[int, int, int, int]]:
		model = "hog" if self._config.get_processing_mode() == "CPU" else "gnn"
		return face_recognition.face_locations(frame, model=model)

	def _get_known_encodings(self) -> List[numpy.ndarray]:
		current_students = self._context.get_students()
		current_count = len(current_students)
		
		if not self._encoding_cache_valid or current_count != self._last_student_count or self._cached_encodings is None:
			self._cached_encodings = [student.get_face_encode() for student in current_students]
			self._last_student_count = current_count
			self._encoding_cache_valid = True
		
		return self._cached_encodings

	@error_handler
	def _encode_faces(self, frame: numpy.ndarray, face_locations: List[Tuple[int, int, int, int]]) -> List[numpy.ndarray]:
		return face_recognition.face_encodings(frame, face_locations)

	@error_handler
	def _compare_faces(self, known_encodings: List[numpy.ndarray], cam_face_encodings: List[numpy.ndarray]) -> List[bool]:
		return face_recognition.compare_faces(known_encodings, cam_face_encodings, tolerance=0.5)

	@error_handler
	def _process_matches(self, matches: List[bool]) -> None:
		students = self._context.get_students()
		for i, match in enumerate(matches):
			if match and i < len(students):
				with self._scan_lock:
					student = students[i]
					if not student.is_attended():
						self._record_attendance(student)
						Thread(target=winsound.Beep, args=(2500, 500)).start()
	
	def invalidate_cache(self) -> None:
		self._encoding_cache_valid = False
		self._cached_encodings = None
		self._last_student_count = 0

	@error_handler
	def _record_attendance(self, student: Student) -> None:
		self._config.frame_processing_executor.submit(
			self.attendace_controller.insert_attendance,
			student.student_id,
			f"{student.first_name} {student.last_name}"
		)
		student.confirm_attendance()
