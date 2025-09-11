import os
import sys
import customtkinter

from app.config.configrations import Configrations
from app.config.router import Router
from app.views.students import Students
from app.views.courses import Courses
from app.views.users import Users
from app.views.login import Login
from app.controllers.courses import get_courses
from app.controllers.students import get_students
from app.controllers.users import fetch_users
from app.helper.error_handler import error_handler

customtkinter.set_appearance_mode("dark")

class Main():
  def __init__(self):
    self._config = Configrations()
    self._router = Router()

    get_courses()
    get_students()
    fetch_users()

  @error_handler
  def create_navbar(self):
    navbar = customtkinter.CTkFrame(self._config.window)
    navbar.pack(fill=customtkinter.X)

    students_view = customtkinter.CTkButton(
      navbar,
      corner_radius = 0,
      command = lambda: self._router.navigate(Students),
      text = "Students"
    )
    students_view.pack(side=customtkinter.LEFT)

    courses_view = customtkinter.CTkButton(
      navbar,
      corner_radius=0,
      command= lambda: self._router.navigate(Courses),
      text="Courses"
    )
    courses_view.pack(side=customtkinter.LEFT)

    users_view = customtkinter.CTkButton(
      navbar,
      corner_radius=0,
      command= lambda:  self._router.navigate(Users),
      text="Users"
    )
    users_view.pack(side=customtkinter.LEFT)

  @error_handler
  def when_app_close(self):
    self._config.window.destroy()
    self._config.shutdown_event.set()
    self._config.pause_event.set()
    self._config.executor.shutdown(wait=True)

    sys.exit(0)

  @error_handler
  def start_program(self):
    try:
      self.window = customtkinter.CTk()
      self._config.set_window(self.window)

      width = self.window.winfo_screenwidth()
      height = self.window.winfo_screenheight()

      self.window.geometry("%dx%d" % (width, height))
      self.window.title("TrueFace Admin")
      # self.window.iconbitmap("logo.ico")
      self.window.protocol("WM_DELETE_WINDOW", self.when_app_close)

      self.create_navbar()
      self._router.navigate(Students)

      self.window.mainloop()

    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
  Main().start_program()
  # Login().launch_view()