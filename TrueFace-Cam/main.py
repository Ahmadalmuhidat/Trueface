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
from CTkMessagebox import CTkMessagebox
from app.config.router import Router

class Main:
  def __init__(self):
    try:
      self._config = Configrations()
      self._camera_manager = CameraManager()
      self._router = Router()
      self.window = None

    except Exception:
      self._log_exception()

  def create_navbar(self):
    """Build the navigation bar and buttons."""
    try:
      navbar = customtkinter.CTkFrame(self.window)
      navbar.pack(fill=customtkinter.X)

      self._add_nav_button(navbar, "Home", Home.Home)
      self._add_nav_button(navbar, "Attendance", Attendance.Attendance)
      self._add_nav_button(navbar, "Students", Students.Students)
      self._add_nav_button(navbar, "Settings", Settings.Settings)

    except Exception:
      self._log_exception()

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
        self._show_message("Error", "Please stop the camera first", "cancel")
        return

      # TODO: Shut down all threads if applicable
      self.window.destroy()
      sys.exit(0)

    except Exception:
      self._log_exception()

  def start_program(self):
    """Initialize and start the main application."""
    try:
      self._init_window()
      self._config.set_window(self.window)
      self._camera_manager.scan_connected_cameras()

      self.create_navbar()
      self._router.navigate(Home.Home)

      self.window.mainloop()

    except Exception:
      self._log_exception()
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

  def _show_message(self, title, message, icon):
    CTkMessagebox(title=title, message=message, icon=icon)

  def _log_exception(self):
    """Log exception details for debugging."""
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)

if __name__ == "__main__":
  # Main().start_program()
  Login.Login().launch_view()
