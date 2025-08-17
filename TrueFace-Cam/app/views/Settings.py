import os
import sys
import customtkinter

from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.classes import get_classes_by_teacher
from app.controllers.attendance import get_attendance_by_class
from app.controllers.students import get_students_by_class
from CTkMessagebox import CTkMessagebox

class Settings():
  def __init__(self):
    from app.core.camera_manager import CameraManager

    self._camera_manager = CameraManager()
    self._context = Context()
    self._config = Configrations()

    self.current_class_entry = None
    self.available_cameras_entry = None

    self._load_classes()
    self._load_cameras()

  def _load_classes(self):
    """Fetch classes for the current teacher and prepare ID-title map."""
    get_classes_by_teacher()
    self.class_id_title_map = {
      f"{camera.subject_area} {camera.start_time}-{camera.end_time}": camera.class_id
      for camera in self._context.get_classes()
    }

  def _load_cameras(self):
    """Fetch available cameras and prepare name-index map."""
    self.cameras_key_map = {
      cam.get_name(): cam.get_index()
      for cam in self._camera_manager.camera_scanner.get_available_cameras()
    }

  def update_current_camera(self, user_camera_selection):
    """Set the selected camera as current."""
    self._camera_manager.set_current_camera(self.cameras_key_map.get(user_camera_selection))
    self._show_message("Info", "Camera has been updated", "check")

  def update_class(self):
    """Set the selected class as current and fetch attendance."""
    self._config.loading_cursor_on()
    try:
      selected_id = self.class_id_title_map.get(self.current_class_entry.get())
      ClassObject = next(
        (class_ for class_ in self._context.get_classes() if class_.class_id == selected_id),
        None
      )
      self._context.set_current_class(ClassObject)
      get_attendance_by_class()
      get_students_by_class()

    finally:
      self._config.loading_cursor_off()

    self._show_message("Info", "Class has been updated", "check")

  def _show_message(self, title, message, icon):
    CTkMessagebox(title=title, message=message, icon=icon)

  def launch_view(self, parent):
    try:
      content_frame = customtkinter.CTkFrame(parent)
      content_frame.pack(
        padx = 20,
        pady = 20
      )

      current_class_label = customtkinter.CTkLabel(
        content_frame,
        text = "Current class:"
      )
      current_class_label.grid(
        row = 5,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.current_class_entry = customtkinter.CTkComboBox(
        content_frame,
        values = [f"{class_.subject_area} {class_.start_time}-{class_.end_time}" for class_ in self._context.get_classes()],
        width = 400,
        command = lambda _: self._config.frame_processing_executor.submit(self.update_class)
      )
      self.current_class_entry.grid(
        row = 5,
        column = 1,
        padx = 10,
        pady = 10
      )

      available_cameras_label = customtkinter.CTkLabel(
        content_frame,
        text = "Available Cameras:"
      )
      available_cameras_label.grid(
        row = 7,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.available_cameras_entry = customtkinter.CTkComboBox(
        content_frame,
        values = list(self.cameras_key_map.keys()),
        width = 400,
        command = self.update_current_camera
      )
      self.available_cameras_entry.grid(
        row = 7,
        column = 1,
        padx = 10,
        pady = 10
      )
      self.available_cameras_entry.set(self.cameras_key_map.get(self._camera_manager.get_current_camera()) or "No Camera Selected")

      view_camera_button = customtkinter.CTkButton(
        content_frame,
        text = "Test Current Camera",
        command = self._camera_manager.view_current_camera_stream
      )
      view_camera_button.grid(
        row = 8,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)