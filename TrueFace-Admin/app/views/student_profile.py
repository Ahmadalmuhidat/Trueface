import customtkinter
import uuid
import gc

from app.config.context import Context
from app.interfaces.lecture import Lecture
from app.config.configurations import Configurations
from app.controllers.lectures import LecturesController
from app.controllers.students import StudentsController
from app.utils.error_handler import error_handler

class StudentProfile:
  def __init__(self):
    self._context = Context()
    self._config = Configurations()

    self.lectures = self._context.get_current_student().get_lectures()
    self.lectures_controller = LecturesController()
    self.students_controller = StudentsController()
    self.available_lectures = self.lectures_controller.get_all_lectures()
    self.lectures_rows = []
    self.headers =  [
      "Subject",
      "Start Time",
      "End Time",
      "Day",
      ""
    ]

  # --------------------
  # operations
  # --------------------

  def _search(self, term: str) -> None:
    self.lectures = self._context.get_current_student().search_lecture(term)
    self._display_lectures_table()

  @error_handler
  def _delete(self, lecture: Lecture):
    if self.students_controller.remove_student_from_lecture(self._context.get_current_student(), lecture):
      self._refresh_lectures_table()

  @error_handler
  def _create(self):
    selected_lecture = next((lecture for lecture in self.available_lectures if f"{lecture.subject_area} {lecture.start_time}-{lecture.end_time}" == self.lecture_entry.get()), None)
    selected_lecture.day = self.day_entry.get()

    if self.students_controller.add_student_to_lecture(uuid.uuid4(), self._context.get_current_student(), selected_lecture):
      self._refresh_lectures_table()

  # --------------------
  # forms
  # --------------------

  @error_handler
  def _submit_lecture_form(self):
    pop_window = customtkinter.CTkToplevel()
    pop_window.grab_set()
    pop_window.geometry("490x410")
    pop_window.resizable(False, False)
    pop_window.title("Add New Lecture")

    lecture_label = customtkinter.CTkLabel(pop_window, text="Select Lecture:")
    lecture_label.pack(padx=10, pady=10)

    self.lecture_entry = customtkinter.CTkComboBox(
      pop_window,
      values=[f"{lec.subject_area} {lec.start_time}-{lec.end_time}" for lec in self.available_lectures],
      width=350,
    )
    self.lecture_entry.pack(padx=10, pady=10)
    self.lecture_entry.set("None")

    day_label = customtkinter.CTkLabel(pop_window, text="Select Day:")
    day_label.pack(padx=10, pady=10)

    self.day_entry = customtkinter.CTkComboBox(
      pop_window,
      values=[
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
      ],
      width=350,
    )
    self.day_entry.pack(padx=10, pady=10)
    self.day_entry.set("None")

    submit_button = customtkinter.CTkButton(
      pop_window,
      text="Save Lecture",
      command=lambda: self._create()
    )
    submit_button.pack(padx=10, pady=5)

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _add_lecture_row(self, lecture: Lecture, row):
    lecture_row = [
      lecture.subject_area,
      lecture.start_time,
      lecture.end_time,
      lecture.day
    ]

    for col, data in enumerate(lecture_row):
      lecture_data = customtkinter.CTkLabel(
        self.lectures_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      lecture_data.grid(row=row, column=col, sticky="nsew")
      self.lectures_rows.append(lecture_data)

    delete_button = customtkinter.CTkButton(
      self.lectures_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._delete(lecture)
    )
    delete_button.grid(
      row=row,
      column=len(lecture_row),
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.lectures_rows.append(delete_button)

  @error_handler
  def _clear_lectures_table(self):
    for widget in self.lectures_rows:
      try:
        widget.destroy()
      except:
        pass
    self.lectures_rows.clear()
    
    if len(self.lectures) > 100:
      gc.collect()

  def _refresh_lectures_table(self):
    self._context.get_current_student().fetch_lectures()
    self.lectures = self._context.get_current_student().get_lectures()
    self._display_lectures_table()

  @error_handler
  def _display_lectures_table(self):
    self._clear_lectures_table()

    for row, lecture in enumerate(self.lectures, start=1):
      self._add_lecture_row(lecture, row)

    self.lectures_count.configure(text=f"Results: {len(self.lectures)}")

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self, parent: customtkinter.CTkFrame):
    search_bar_frame = customtkinter.CTkFrame(
      parent,
      bg_color="transparent"
    )
    search_bar_frame.pack(
      fill="x",
      expand=False
    )

    search_button = customtkinter.CTkButton(
      search_bar_frame,
      command=lambda: self._search(search_bar.get()),
      text="Search"
    )
    search_button.grid(
      row=0,
      column=0,
      sticky="nsew",
      pady=10,
      padx=5
    )

    search_bar = customtkinter.CTkEntry(
      search_bar_frame,
      width=400,
      placeholder_text="Search for Lectures..."
    )
    search_bar.grid(
      row=0,
      column=1,
      sticky="nsew",
      pady=10
    )

    refresh_button = customtkinter.CTkButton(
      search_bar_frame,
      width=100,
      text="Refresh",
       command=self._refresh_lectures_table
    )
    refresh_button.grid(
      row=0,
      column=4,
      sticky="nsew",
      pady=10,
      padx=5
    )

    add_lecture_button = customtkinter.CTkButton(
      search_bar_frame,
      width=100,
      text="Add Lecture",
      command=self._submit_lecture_form
    )
    add_lecture_button.grid(
      row=0,
      column=5,
      sticky="nsew",
      pady=10,
      padx=5
    )

    self.lectures_count = customtkinter.CTkLabel(search_bar_frame)
    self.lectures_count.grid(
      row=0,
      column=7,
      padx=10,
      pady=5
    )

    self.lectures_table_frame = customtkinter.CTkScrollableFrame(parent)
    self.lectures_table_frame.pack(
      fill="both",
      expand=True
    )

    for col, header in enumerate(self.headers):
      header_label = customtkinter.CTkLabel(
        self.lectures_table_frame,
        text=header,
        padx=10,
        pady=10
      )
      header_label.grid(
        row=0,
        column=col,
        sticky="nsew"
      )

    for col in range(len(self.headers)):
      self.lectures_table_frame.columnconfigure(col, weight=1)
    
    self._display_lectures_table()
