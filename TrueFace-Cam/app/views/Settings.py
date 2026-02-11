import customtkinter
import requests
import json

from requests.exceptions import Timeout, RequestException
from app.config.context import Context
from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler
from app.controllers.lectures import LectureController

class Settings():
  def __init__(self):
    from app.core.camera_manager import CameraManager

    self._camera_manager = CameraManager()
    self._context = Context()
    self._config = Configurations()
    self._alert = AlertsManager()
    self._lectures_loaded = False
    self._cameras_loaded = False
    self._loading_indicators = {}
    self._lecture_controller = LectureController()

    self.current_lecture_entry = None
    self.available_cameras_entry = None
    self.lecture_id_title_map = {}
    self.cameras_key_map = {}

    self._load_lectures()
    self._load_cameras()

  # --------------------
  # operations
  # --------------------

  @error_handler
  def _load_lectures(self):
    if self._lectures_loaded:
      return

    if hasattr(self, 'current_lecture_entry') and self.current_lecture_entry:
      self.current_lecture_entry.configure(values=["Loading lectures..."])

    def _load_lectures_async():
      try:
        self._lecture_controller.get_lectures_by_teacher()
        self.lecture_id_title_map = {
          f"{lecture.subject_area} {lecture.start_time}-{lecture.end_time}": lecture.lecture_id
          for lecture in self._context.get_lectures()
        }
        self._lectures_loaded = True

        if hasattr(self, 'current_lecture_entry') and self.current_lecture_entry:
          lecture_values = [f"{lecture.subject_area} {lecture.start_time}-{lecture.end_time}" for lecture in self._context.get_lectures()]
          self.current_lecture_entry.configure(values=lecture_values)
          if lecture_values:
            self.current_lecture_entry.set(lecture_values[0])

      except Exception as e:
        self._alert.error(f"Failed to load lectures: {str(e)}")
        if hasattr(self, 'current_lecture_entry') and self.current_lecture_entry:
          self.current_lecture_entry.configure(values=["Failed to load lectures"])

    self._config.ui_threads_executor.submit(_load_lectures_async)

  @error_handler
  def _load_cameras(self):
    if self._cameras_loaded:
      return

    if hasattr(self, 'available_cameras_entry') and self.available_cameras_entry:
      self.available_cameras_entry.configure(values=["Loading cameras..."])

    def _load_cameras_async():
      try:
        available_cameras = self._camera_manager.camera_scanner.get_available_cameras()

        if not available_cameras:
          self._camera_manager.camera_scanner.scan_connected_cameras()
          available_cameras = self._camera_manager.camera_scanner.get_available_cameras()

        self.cameras_key_map = {
          cam.get_name(): cam.get_index()
          for cam in available_cameras
        }
        self._cameras_loaded = True

        if hasattr(self, 'available_cameras_entry') and self.available_cameras_entry:
          camera_values = list(self.cameras_key_map.keys())
          self.available_cameras_entry.configure(values=camera_values)

          if camera_values:
            self.available_cameras_entry.set(camera_values[0])

      except Exception as e:
        self._alert.error(f"Failed to load cameras: {str(e)}")
        if hasattr(self, 'available_cameras_entry') and self.available_cameras_entry:
          self.available_cameras_entry.configure(values=["Failed to load cameras"])

    self._config.ui_threads_executor.submit(_load_cameras_async)

  @error_handler
  def _update_current_lecture(self):
    if not self._lectures_loaded:
      self._alert.warning("Lectures are still loading, please wait...")
      return
    
    def _update_lecture_async():
      self._config.loading_cursor_on()
      try:
        selected_id = self.lecture_id_title_map.get(self.current_lecture_entry.get())
        LectureObject = next(
          (lecture for lecture in self._context.get_lectures() if lecture.lecture_id == selected_id),
          None
        )
        self._context.set_current_lecture(LectureObject)
        self._context.fetch_students()
        self._alert.success("Lecture has been updated")

      except Exception as e:
        self._alert.error(f"Failed to update lecture: {str(e)}")
      finally:
        self._config.loading_cursor_off()

    self._config.ui_threads_executor.submit(_update_lecture_async)

  @error_handler
  def _update_current_camera(self, user_camera_selection: str):
    self._camera_manager.set_current_camera_index(self.cameras_key_map.get(user_camera_selection))
    self._alert.success("Camera has been updated")

  @error_handler
  def _check_api_health(self):
    def _check_api_async():
      try:
        original = self._config.get_backend_ip_address()
        self._config.set_backend_ip_address(self.server_api_entry.get())
        response = requests.get(self._config.get_backend_endpoint(), timeout=3)

        if response.status_code == 200:
          try:
            api_active = response.json()
            if api_active.get("data"):
              self._alert.success(f"{self.server_api_entry.get()} server is working fine")
            else:
              self._alert.error(f"{self.server_api_entry.get()} does not work")
              self._config.set_backend_ip_address(original)
          except json.JSONDecodeError:
            self._alert.error(f"Invalid response from {self.server_api_entry.get()}")
            self._config.set_backend_ip_address(original)
        else:
          self._alert.error(f"{self.server_api_entry.get()} returned status {response.status_code}")
          self._config.set_backend_ip_address(original)

      except Timeout:
        self._alert.error(f"{self.server_api_entry.get()} did not respond in time")
        self._config.set_backend_ip_address(original)
      except RequestException as e:
        self._alert.error(f"An error occurred: {str(e)}")
        self._config.set_backend_ip_address(original)

    self._config.ui_threads_executor.submit(_check_api_async)

  @error_handler
  def _refresh_lectures(self):
    self._lectures_loaded = False
    self._load_lectures()

  @error_handler
  def _refresh_cameras(self):
    self._cameras_loaded = False
    self._load_cameras()

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self, parent):
    content_frame = customtkinter.CTkFrame(parent)
    content_frame.pack(
      padx=20,
      pady=20
    )

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
      values=["Loading lectures..."],
      width=300,
      command=lambda _: self._update_current_lecture()
    )
    self.current_lecture_entry.grid(
      row=5,
      column=1,
      padx=10,
      pady=10
    )

    refresh_lectures_button = customtkinter.CTkButton(
      content_frame,
      text="Refresh",
      width=100,
      command=self._refresh_lectures
    )
    refresh_lectures_button.grid(
      row=5,
      column=2,
      padx=5,
      pady=10
    )

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
      values=["Loading cameras..."],
      width=300,
      command=self._update_current_camera
    )
    self.available_cameras_entry.grid(
      row=7,
      column=1,
      padx=10,
      pady=10
    )

    scan_cameras_button = customtkinter.CTkButton(
      content_frame,
      text="Scan Cameras",
      width=140,
      command=self._refresh_cameras
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