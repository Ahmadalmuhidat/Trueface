import os
import sys
import customtkinter

import app.views.login as Login
import app.views.home as Home
import app.views.attendance as Attendance
import app.views.settings as Settings
import app.views.students as Students

from app.config.configrations import Configrations
from app.core.camera_manager import CameraManager
from app.config.router import Router
from app.helper.logger import Logger
from app.helper.alerts_manager import AlertsManager

customtkinter.set_appearance_mode("dark")

class Main:
  def __init__(self):
    try:
      self._config = Configrations()
      self._camera_manager = CameraManager()
      self._router = Router()
      self._logger = Logger()
      self._alert = AlertsManager()

      self.window = None

    except Exception as e:
      self._logger.log_exception(e)

  def create_navbar(self):
    """Build the navigation bar and buttons."""
    try:
      navbar = customtkinter.CTkFrame(self.window)
      navbar.pack(fill=customtkinter.X)

      self._add_nav_button(navbar, "Home", Home.Home)
      self._add_nav_button(navbar, "Attendance", Attendance.Attendance)
      self._add_nav_button(navbar, "Students", Students.Students)
      self._add_nav_button(navbar, "Settings", Settings.Settings)

    except Exception as e:
      self._logger.log_exception(e)

  def _add_nav_button(self, parent, text, view_class):
    """Helper to add a navigation button."""
    btn = customtkinter.CTkButton(
      parent,
      corner_radius=0,
      command=lambda: self._router.navigate(view_class),
      text=text
    )
    btn.pack(side=customtkinter.LEFT)

  def when_app_close(self):
    """Handle application close event."""
    try:
      if self._camera_manager.get_capturing_is_active():
        self._alert.pop_window("Error", "Please stop the camera first", "cancel")
        return

      self._config.shutdown_event.set()

      self._config.frame_processing_executor.shutdown(wait=True)  
      self._config.ui_threads_executor.shutdown(wait=True)

      self.window.destroy()
      sys.exit(0)

    except Exception as e:
      self._logger.log_exception(e)

  def start_program(self):
    """Initialize and start the main application."""
    try:
      self._init_window()
      self._config.set_window(self.window)
      self._camera_manager.scan_connected_cameras()

      self.create_navbar()
      self._router.navigate(Home.Home)

      self.window.mainloop()

    except Exception as e:
      self._logger.log_exception(e)
    except KeyboardInterrupt:
      pass

  def _init_window(self):
    """Set up main application window."""
    self.window = customtkinter.CTk()

    # Fullscreen dimensions
    width = self.window.winfo_screenwidth()
    height = self.window.winfo_screenheight()
    self.window.geometry(f"{width}x{height}")

    # Icon, title, close protocol
    self.window.iconbitmap("logo.ico")
    self.window.title("TrueFace Camera")
    self.window.protocol("WM_DELETE_WINDOW", self.when_app_close)

if __name__ == "__main__":
  # Main().start_program()
  Login.Login().launch_view()
