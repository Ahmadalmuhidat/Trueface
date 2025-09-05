import customtkinter
import uuid

from app.config.context import Context
from app.interfaces.lecture import Lecture
from app.config.configrations import Configrations
from app.helper.lectures import get_all_lectures
from app.controllers.students import remove_student_from_lecture, add_student_to_lecture
from app.helper.error_handler import error_handler

class StudentProfile:
  def __init__(self):
    self._context = Context()
    self._config = Configrations()

    self.lectures = self._context.get_current_student().get_lectures()
    self.lectures_rows = []
    self.headers =  [
      "Subject",
      "Start Time",
      "End Time",
      "Day",
      ""
    ]
    self.available_lectures = get_all_lectures()

  # --------------------
  # operations
  # --------------------

  def _search(self, term: str) -> None:
    self.lectures = self._context.get_current_student().search_leacture(term)
    self._display_lectures_table()

  @error_handler
  def _delete(self, lecture: Lecture):
    self._config.loading_cursor_on()
    remove_student_from_lecture(self._context.get_current_student(), lecture)
    self._context.get_current_student().remove_lecture(lecture.lecture_id)
    self.lectures = self._context.get_current_student().get_lectures()
    self._config.loading_cursor_off()
    self._display_lectures_table()

  def _refresh_lectures_table(self):
    self._context.get_current_student().fetch_lectures()
    self._display_lectures_table()

  @error_handler
  def _submit_new_lecture(self):
    self._config.loading_cursor_on()
    selected_lecture = next((lecture for lecture in self.available_lectures if f"{lecture.subject_area} {lecture.start_time}-{lecture.end_time}" == self.lecture_entry.get()), None)
    selected_day = self.day_entry.get()

    if not selected_lecture or not selected_day:
      return

    add_student_to_lecture(uuid.uuid4(), self._context.get_current_student(), selected_lecture, selected_day)
    self.lectures.append(selected_lecture)
    self._add_lecture_row(selected_lecture, len(self.lectures) + 1)
    self._config.loading_cursor_off()

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

    class_label = customtkinter.CTkLabel(pop_window, text="Select Lecture:")
    class_label.pack(padx=10, pady=10)

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
      text="Save Class",
      command=lambda: self._submit_new_lecture()
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
      class_data = customtkinter.CTkLabel(
        self.lectures_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      class_data.grid(row=row, column=col, sticky="nsew")
      self.lectures_rows.append(class_data)

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
      widget.destroy()
    self.lectures_rows.clear()

  @error_handler
  def _display_lectures_table(self):
    self._config.loading_cursor_on()
    self._clear_lectures_table()

    for row, lecture in enumerate(self.lectures, start=1):
      self._add_lecture_row(lecture, row)

    self.students_count.configure(text=f"Results: {len(self.lectures)}")
    self._config.loading_cursor_off()

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

    self.students_count = customtkinter.CTkLabel(search_bar_frame)
    self.students_count.grid(
      row=0,
      column=6,
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

    self._config.executor.submit(self._display_lectures_table)
