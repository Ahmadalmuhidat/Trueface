import os
import sys
import customtkinter

from app.views.Login import Login
from app.views.Home import Home
from app.views.Attendance import Attendance
from app.views.Settings import Settings
from app.views.Students import Students
from app.config.configurations import Configurations
from app.core.camera_manager import CameraManager
from app.config.router import Router
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler
from app.config.context import Context

customtkinter.set_appearance_mode("dark")

class Main:
  def __init__(self):
    self._config = Configurations()
    self._context = Context()
    self._camera_manager = CameraManager()
    self._router = Router()
    self._alert = AlertsManager()

    self.window = None

    self._context.fetch_lectures()

  @error_handler
  def create_navbar(self):
    navbar = customtkinter.CTkFrame(self.window)
    navbar.pack(fill=customtkinter.X)

    self._add_nav_button(navbar, "Home", Home)
    self._add_nav_button(navbar, "Attendance", Attendance)
    self._add_nav_button(navbar, "Students", Students)
    self._add_nav_button(navbar, "Settings", Settings)

  @error_handler
  def _add_nav_button(self, parent, text, view_class):
    btn = customtkinter.CTkButton(
      parent,
      corner_radius=0,
      command=lambda: self._router.navigate(view_class),
      text=text
    )
    btn.pack(side=customtkinter.LEFT)

  @error_handler
  def when_app_close(self):
    try:
      if self._camera_manager.is_capturing():
        self._alert.error("Please stop the camera first")
        return

      home_view = Home()

      self._config.shutdown_event.set()

      self._config.frame_processing_executor.shutdown(wait=True)  
      self._config.ui_threads_executor.shutdown(wait=True)

      self.window.destroy()
      sys.exit(0)

    except Exception as e:
      pass

  @error_handler
  def start_program(self):
    try:
      self._init_window()
      self._config.set_window(self.window)
      self._camera_manager.scan_connected_cameras()

      self.create_navbar()
      self._router.navigate(Home)

      self.window.mainloop()

    except KeyboardInterrupt:
      pass

  @error_handler
  def _init_window(self):
    self.window = customtkinter.CTk()

    width = self.window.winfo_screenwidth()
    height = self.window.winfo_screenheight()

    self.window.geometry(f"{width}x{height}")
    self.window.iconbitmap("logo.ico")
    self.window.title("TrueFace Camera")
    self.window.protocol("WM_DELETE_WINDOW", self.when_app_close)

if __name__ == "__main__":
  # Main().start_program()
  Login().launch_view()
