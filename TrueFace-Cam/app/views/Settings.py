import os
import sys
import customtkinter
import requests
import json

from requests.exceptions import Timeout, RequestException
from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.lectures import get_lectures_by_teacher
from app.controllers.students import get_students_by_lecture
from app.helper.alerts_manager import AlertsManager

class Settings():
  def __init__(self):
    from app.core.camera_manager import CameraManager

    self._camera_manager = CameraManager()
    self._context = Context()
    self._config = Configrations()
    self._alert = AlertsManager()

    self.current_lecture_entry = None
    self.available_cameras_entry = None

    self._load_lectures()
    self._load_cameras()

  def _load_lectures(self):
    get_lectures_by_teacher()
    self.class_id_title_map = {
      f"{camera.subject_area} {camera.start_time}-{camera.end_time}": camera.class_id
      for camera in self._context.get_lectures()
    }

  def _load_cameras(self):
    self.cameras_key_map = {
      cam.get_name(): cam.get_index()
      for cam in self._camera_manager.camera_scanner.get_available_cameras()
    }

  def _update_current_camera(self, user_camera_selection):
    self._camera_manager.set_current_camera(self.cameras_key_map.get(user_camera_selection))
    self._alert.pop_window(
      "Info",
      "Camera has been updated",
      "check"
    )

  def _check_api_health(self):
    try:
      # Backup the original backend endpoint
      original = self._config.get_backend_endpoint()
      self._config.set_backend_ip_address(self.server_api_entry.get())
      response = requests.get(self._config.get_backend_endpoint(), timeout=5)

      if response.status_code == 200:
        try:
          api_active = response.json()
          if api_active.get("data"):
            self._alert.pop_window(
              "Backend Endpoint Status",
              f"{self.server_api_entry.get()} is working fine",
              "check"
            )
          else:
            self._alert.pop_window(
              "Backend Endpoint Status",
              f"{self.server_api_entry.get()} does not work",
              "cancel"
            )
            self._config.set_backend_ip_address(original)
        except json.JSONDecodeError:
          self._alert.pop_window(
            "Backend Endpoint Status",
            f"Invalid response from {self.server_api_entry.get()}",
            "cancel"
          )
          self._config.set_backend_ip_address(original)
      else:
        self._alert.pop_window(
          "Backend Endpoint Status",
          f"{self.server_api_entry.get()} returned status {response.status_code}",
          "cancel"
        )
        self._config.set_backend_ip_address(original)
    
    except Timeout:
      self._alert.pop_window(
        "Backend Endpoint Status",
        f"{self.server_api_entry.get()} did not respond in time",
        "cancel"
      )
      self._config.set_backend_ip_address(original)
    except RequestException as e:
      self._alert.pop_window(
        "Backend Endpoint Status",
        f"An error occurred: {str(e)}",
        "cancel"
      )
      self._config.set_backend_ip_address(original)

  def _update_lecture(self):
    self._config.loading_cursor_on()
    try:
      selected_id = self.class_id_title_map.get(self.current_lecture_entry.get())
      ClassObject = next(
        (lecture for lecture in self._context.get_lectures() if lecture.class_id == selected_id),
        None
      )
      self._context.set_current_lecture(ClassObject)
      get_students_by_lecture()

    finally:
      self._config.loading_cursor_off()

    self._alert.pop_window(
      "Info",
      "Lecture has been updated",
      "check"
    )

  def launch_view(self, parent):
    try:
      content_frame = customtkinter.CTkFrame(parent)
      content_frame.pack(
        padx=20,
        pady=20
      )

      # Current Lecture
      current_lecture_label = customtkinter.CTkLabel(
        content_frame,
        text="Current Lecture:"
      )
      current_lecture_label.grid(
        row=5,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
      )

      self.current_lecture_entry = customtkinter.CTkComboBox(
        content_frame,
        values=[f"{lecture.subject_area} {lecture.start_time}-{lecture.end_time}" for lecture in self._context.get_lectures()],
        width=300,
        command=lambda _: self._config.frame_processing_executor.submit(self._update_lecture)
      )
      self.current_lecture_entry.grid(
        row=5,
        column=1,
        padx=10,
        pady=10
      )

      # Available Cameras
      available_cameras_label = customtkinter.CTkLabel(
        content_frame,
        text="Available Cameras:"
      )
      available_cameras_label.grid(
        row=7,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
      )

      self.available_cameras_entry = customtkinter.CTkComboBox(
        content_frame,
        values=list(self.cameras_key_map.keys()),
        width=300,
        command=self._update_current_camera
      )
      self.available_cameras_entry.grid(
        row=7,
        column=1,
        padx=10,
        pady=10
      )
      self.available_cameras_entry.set(
        self.cameras_key_map.get(self._camera_manager.get_current_camera()) or "No Camera Selected"
      )

      scan_cameras_button = customtkinter.CTkButton(
        content_frame,
        text="Scan Cameras",
        width=140,
        command=lambda: self._camera_manager.camera_scanner.scan_connected_cameras()
      )
      scan_cameras_button.grid(
        row=7,
        column=2,
        padx=5,
        pady=10
      )

      view_camera_button = customtkinter.CTkButton(
        content_frame,
        text="Test Camera",
        width=140,
        command=self._camera_manager.view_current_camera_stream
      )
      view_camera_button.grid(
        row=7,
        column=3,
        padx=5,
        pady=10
      )

      # Server API
      server_label = customtkinter.CTkLabel(
        content_frame,
        text="Server API URL:"
      )
      server_label.grid(
        row=10,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
      )

      self.server_api_entry = customtkinter.CTkEntry(
        content_frame,
        width=300,
      )
      self.server_api_entry.grid(
        row=10,
        column=1,
        padx=10,
        pady=10
      )
      self.server_api_entry.insert(0, self._config.get_backend_ip_address())

      check_api_button = customtkinter.CTkButton(
        content_frame,
        text="Check Health",
        width=140,
        command=lambda: self._check_api_health()
      )
      check_api_button.grid(
        row=10,
        column=2,
        padx=10,
        pady=1
      )

      # Processing Mode
      processing_label = customtkinter.CTkLabel(
        content_frame,
        text="Processing Mode:"
      )
      processing_label.grid(
        row=12,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
      )

      self.processing_mode_entry = customtkinter.CTkComboBox(
        content_frame,
        values=["CPU", "GPU"],
        width=300,
        command=lambda choice: self._config.set_processing_mode(choice)
      )
      self.processing_mode_entry.grid(
        row=12,
        column=1,
        padx=10,
        pady=10
      )
      self.processing_mode_entry.set(self._config.get_processing_mode())

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)