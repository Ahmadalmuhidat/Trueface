import sys
import customtkinter

from app.config.configurations import Configurations
from app.config.router import Router
from app.views.students import Students
from app.views.courses import Courses
from app.views.users import Users
from app.utils.error_handler import error_handler
from app.config.context import Context

customtkinter.set_appearance_mode("dark")

class Main():
  def __init__(self):
    self._config = Configurations()
    self._context = Context()
    self._router = Router()
    self._data_loaded = False

  def _fetch_data_async(self):
    def fetch_data():
      try:
        self._config.loading_cursor_on()
        self._context.fetch_courses()
        self._context.fetch_students()
        self._context.fetch_users()
        self._config.loading_cursor_off()

        self._data_loaded = True
        
        if hasattr(self, 'window'):
          self.window.after(0, self._on_data_loaded)
      except Exception as e:
        self._data_loaded = False
    
    self._config.executor.submit(fetch_data)

  def _on_data_loaded(self):
    self._router.navigate(Students)

  @error_handler
  def create_navbar(self):
    navbar = customtkinter.CTkFrame(self._config.window)
    navbar.pack(fill=customtkinter.X)

    students_view = customtkinter.CTkButton(
      navbar,
      corner_radius = 0,
      command = lambda: self._navigate_to_view(Students),
      text = "Students"
    )
    students_view.pack(side=customtkinter.LEFT)

    courses_view = customtkinter.CTkButton(
      navbar,
      corner_radius=0,
      command= lambda: self._navigate_to_view(Courses),
      text="Courses"
    )
    courses_view.pack(side=customtkinter.LEFT)

    users_view = customtkinter.CTkButton(
      navbar,
      corner_radius=0,
      command= lambda: self._navigate_to_view(Users),
      text="Users"
    )
    users_view.pack(side=customtkinter.LEFT)

  def _navigate_to_view(self, view_class):
    if not self._data_loaded:
      return

    self._router.navigate(view_class)

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
      
      self._fetch_data_async()

      self.window.mainloop()

    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
  Main().start_program()
  # Login().launch_view()
