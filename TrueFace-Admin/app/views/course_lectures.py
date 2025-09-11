import customtkinter

from app.interfaces.lecture import Lecture
from app.config.context import Context
from app.config.configrations import Configrations
from app.interfaces.lecture import Lecture
from app.controllers.lectures import add_lecture, remove_lecture, update_lecture
from app.helper.error_handler import error_handler
from app.helper.time import convert_to_24h

class Lectures():
  def __init__(self):
    self._context = Context()
    self._config = Configrations()

    self.lectures = self._context.get_current_course().get_lectures()
    self.lectures_rows = []
    self.headers = [
      "Classe ID",
      "Subject",
      "Catalog NBR",	
      "Academic Career",	
      "Course Offering NBR",	
      "Start Time",	
      "End Time",	
      "Section",	
      "Component",	
      "Campus",	
      "Instructor ID",	
      "Instructor Type"
    ]

  # --------------------
  # operations
  # --------------------

  def _search_lecture(self, term: str) -> None:
    self.lectures = self._context.get_current_course().search_leacture(term)
    self._display_lectures_table()

  @error_handler
  def _delete_lecture(self, lecture_id):
    self._config.loading_cursor_on()
    remove_lecture(lecture_id)
    self._context.get_current_course().remove_lecture(lecture_id)
    self.lectures = self._context.get_current_course().get_lectures()
    self._config.loading_cursor_off()
    self._display_lectures_table()

  @error_handler
  def _submit_edit_class(self, lecture: Lecture):
    self._config.loading_cursor_on()

    lecture.subject_area = self.subject_entry.get()
    lecture.catalog_nbr = self.catalog_nbr_entry.get()
    lecture.academic_career = self.academic_career_entry.get()
    lecture.offering_nbr = self.offering_nbr_entry.get()
    lecture.section = self.section_entry.get()
    lecture.component = self.component_entry.get()
    lecture.campus = self.campus_entry.get()
    lecture.instructor.instructor_id = next((user.user_id for user in self._context.get_users() if user.name == self.instructor_id_entry.get()), None)

    update_lecture(lecture)
    self._refresh_lectures_table()
    self.pop_window.destroy()
    self._config.loading_cursor_off()

  @error_handler
  def _submit_new_lecture(self):
    self._config.loading_cursor_on()

    new_lecture = Lecture(
      self.lecture_id_entry.get(),
      self.subject_entry.get(),
      self.catalog_nbr_entry.get(),
      self.academic_career_entry.get(),
      self._context.get_current_course().course_id,
      self.offering_nbr_entry.get(),
      convert_to_24h(self.start_hour_var.get(), self.start_minute_var.get(), self.start_ampm_var.get()),
      convert_to_24h(self.end_hour_var.get(), self.end_minute_var.get(), self.end_ampm_var.get()),
      self.section_entry.get(),
      self.component_entry.get(),
      self.campus_entry.get(),
      next((user.user_id for user in self._context.get_users() if user.name == self.instructor_id_entry.get()), None)
    )
    add_lecture(new_lecture)

    self.lecture_id_entry.delete(0, customtkinter.END)
    self.subject_entry.delete(0, customtkinter.END)
    self.catalog_nbr_entry.delete(0, customtkinter.END)
    self.academic_career_entry.delete(0, customtkinter.END)
    self.offering_nbr_entry.delete(0, customtkinter.END)
    self.section_entry.delete(0, customtkinter.END)
    self.component_entry.delete(0, customtkinter.END)
    self.campus_entry.delete(0, customtkinter.END)

    self._add_lecture_row(new_lecture, len(self.lectures) + 1)
    self._context.get_current_course().add_lecture(new_lecture)
    self.lectures.append(new_lecture)
    self.lectures_count.configure(text="Results: " + str(len(self.lectures)))
    self._config.loading_cursor_off()

  def _refresh_lectures_table(self):
    self._context.get_current_course().fetch_lectures()
    self._display_lectures_table()

  # --------------------
  # forms
  # --------------------

  def _edit_lecture_form(self, lecture: Lecture):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit Class")
    self.pop_window.geometry("520x520")
    self.pop_window.resizable(False, False)

    entry_w, pad_x, pad_y = 350, 12, 8

    customtkinter.CTkLabel(
      self.pop_window,
      text="Class ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.lecture_id_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.lecture_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.lecture_id_entry.insert(
      0,
      lecture.lecture_id
    )
    self.lecture_id_entry.configure(state="readonly")

    customtkinter.CTkLabel(
      self.pop_window,
      text="Subject:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.subject_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.subject_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.subject_entry.insert(
      0,
      lecture.subject_area
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Catalog NBR:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.catalog_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.catalog_nbr_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.catalog_nbr_entry.insert(
      0,
      lecture.catalog_nbr
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Academic Career:",
      anchor="w"
    ).grid(
      row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.academic_career_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.academic_career_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.academic_career_entry.insert(
      0,
      lecture.academic_career
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Course Offering NBR:",
      anchor="w"
    ).grid(
      row=4,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.offering_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.offering_nbr_entry.grid(
      row=4,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.offering_nbr_entry.insert(
      0,
      lecture.offering_nbr
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Section:",
      anchor="w"
    ).grid(
      row=5,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.section_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.section_entry.grid(
      row=5,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.section_entry.insert(
      0,
      lecture.section
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Component:",
      anchor="w"
    ).grid(
      row=6,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.component_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.component_entry.grid(
      row=6,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.component_entry.insert(
      0,
      lecture.component
    )

    # Campus
    customtkinter.CTkLabel(self.pop_window, text="Campus:", anchor="w").grid(row=7, column=0, padx=pad_x, pady=pad_y, sticky="w")
    self.campus_entry = customtkinter.CTkEntry(self.pop_window, width=entry_w)
    self.campus_entry.grid(row=7, column=1, padx=pad_x, pady=pad_y, sticky="ew")
    self.campus_entry.insert(0, lecture.campus)

    # Instructor
    customtkinter.CTkLabel(self.pop_window, text="Instructor ID:", anchor="w").grid(row=8, column=0, padx=pad_x, pady=pad_y, sticky="w")
    self.instructor_id_entry = customtkinter.CTkComboBox(
        self.pop_window, width=entry_w,
        values=[u.name for u in self._context.get_users()]
    )
    self.instructor_id_entry.grid(row=8, column=1, padx=pad_x, pady=pad_y, sticky="ew")
    self.instructor_id_entry.set(lecture.instructor.name)

    # Submit
    submit_button = customtkinter.CTkButton(
        self.pop_window,
        text="Update Class",
        width=entry_w,
        command=lambda: self._submit_edit_class(lecture)
    )
    submit_button.grid(row=9, column=0, columnspan=2, padx=pad_x, pady=pad_y + 4, sticky="ew")

    self.pop_window.columnconfigure(1, weight=1)

  def _add_lecture_form(self):
    self.course_id_title_map = {
      course.title: course.course_id
      for course in self._context.get_courses()
    }

    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New Class")
    self.pop_window.geometry("520x600")
    self.pop_window.resizable(False, False)

    entry_w, pad_x, pad_y = 350, 12, 8

    customtkinter.CTkLabel(
      self.pop_window,
      text="Class ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.lecture_id_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.lecture_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Subject:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.subject_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.subject_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Catalog NBR:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.catalog_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.catalog_nbr_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Academic Career:",
      anchor="w"
    ).grid(
      row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.academic_career_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.academic_career_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Course Offering NBR:",
      anchor="w"
    ).grid(
      row=4,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.offering_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.offering_nbr_entry.grid(
      row=4,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Start Time:",
      anchor="w"
    ).grid(
      row=5,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    hours = [f"{h:02}" for h in range(1, 13)]
    minutes = [f"{m:02}" for m in range(0, 60)]

    self.start_hour_var = customtkinter.StringVar(value="08")
    self.start_minute_var = customtkinter.StringVar(value="00")
    self.start_ampm_var = customtkinter.StringVar(value="AM")

    self.start_hour_menu = customtkinter.CTkOptionMenu(
      self.pop_window,
      values=hours,
      variable=self.start_hour_var,
      width=80
    )
    self.start_hour_menu.grid(
      row=5,
      column=1,
      padx=(pad_x, 0),
      pady=pad_y,
      sticky="w"
    )

    self.start_minute_menu = customtkinter.CTkOptionMenu(
      self.pop_window,
      values=minutes,
      variable=self.start_minute_var,
      width=80
    )
    self.start_minute_menu.grid(
      row=5,
      column=1,
      padx=(100, 0),
      pady=pad_y,
      sticky="w"
    )

    self.start_ampm_menu = customtkinter.CTkOptionMenu(
      self.pop_window,
      values=["AM", "PM"],
      variable=self.start_ampm_var,
      width=80
    )
    self.start_ampm_menu.grid(
      row=5,
      column=1,
      padx=(190, 0),
      pady=pad_y,
      sticky="w"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="End Time:",
      anchor="w"
    ).grid(
      row=6,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.end_hour_var = customtkinter.StringVar(value="09")
    self.end_minute_var = customtkinter.StringVar(value="00")
    self.end_ampm_var = customtkinter.StringVar(value="AM")

    self.end_hour_menu = customtkinter.CTkOptionMenu(
      self.pop_window,
      values=hours,
      variable=self.end_hour_var,
      width=80
    )
    self.end_hour_menu.grid(
      row=6,
      column=1,
      padx=(pad_x, 0),
      pady=pad_y,
      sticky="w"
    )

    self.end_minute_menu = customtkinter.CTkOptionMenu(
      self.pop_window,
      values=minutes,
      variable=self.end_minute_var,
      width=80
    )
    self.end_minute_menu.grid(
      row=6,
      column=1,
      padx=(100, 0),
      pady=pad_y,
      sticky="w"
    )

    self.end_ampm_menu = customtkinter.CTkOptionMenu(
      self.pop_window, values=["AM", "PM"],
      variable=self.end_ampm_var,
      width=80
    )
    self.end_ampm_menu.grid(
      row=6,
      column=1,
      padx=(190, 0),
      pady=pad_y,
      sticky="w"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Section:",
      anchor="w"
    ).grid(
      row=7,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.section_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.section_entry.grid(
      row=7,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Component:",
      anchor="w"
    ).grid(
      row=8,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.component_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.component_entry.grid(
      row=8,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Campus:",
      anchor="w"
    ).grid(
      row=9,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.campus_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_w
    )
    self.campus_entry.grid(
      row=9,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Instructor ID:",
      anchor="w"
    ).grid(
      row=10,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.instructor_id_entry = customtkinter.CTkComboBox(
      self.pop_window,
      width=entry_w,
      values=[u.name for u in self._context.get_users()]
    )
    self.instructor_id_entry.grid(
      row=10,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    submit_button = customtkinter.CTkButton(
      self.pop_window,
      text="Save Class",
      width=entry_w,
      command=lambda: self._config.executor.submit(self._submit_new_lecture)
    )
    submit_button.grid(
      row=11,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=pad_y + 4,
      sticky="ew"
    )

    self.pop_window.columnconfigure(1, weight=1)

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _add_lecture_row(self, lecture: Lecture, row):
    class_row = [
      lecture.lecture_id,
      lecture.subject_area,
      lecture.catalog_nbr,
      lecture.academic_career,
      lecture.offering_nbr,
      lecture.start_time,
      lecture.end_time,
      lecture.section,
      lecture.component,
      lecture.campus,
      lecture.instructor.name
    ]

    for col, data in enumerate(class_row):
      class_data = customtkinter.CTkLabel(
        self.lectures_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      class_data.grid(row=row, column=col, sticky="nsew")
      self.lectures_rows.append(class_data)

    edit_button = customtkinter.CTkButton(
      self.lectures_table_frame,
      text="Edit",
      command=lambda: self._config.executor.submit(self._edit_lecture_form, lecture)
    )
    edit_button.grid(
      row=row,
      column=11,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.lectures_rows.append(edit_button)

    delete_button = customtkinter.CTkButton(
      self.lectures_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete_lecture, lecture)
    )
    delete_button.grid(
      row=row,
      column=12,
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

    self.lectures_count.configure(
      text="Results: " + str(len(self.lectures))
    )
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
      command=lambda: self._search_lecture(search_bar.get()),
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
      placeholder_text="Search for Classes..."
    )
    search_bar.grid(
      row=0,
      column=1,
      sticky="nsew",
      pady=10
    )

    refresh_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._refresh_lectures_table,
      width=100,
      text="Refresh"
    )
    refresh_button.grid(
      row=0,
      column=4,
      sticky="nsew",
      pady=10,
      padx=5
    )

    add_class_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._add_lecture_form,
      width=100,
      text="Add Class"
    )
    add_class_button.grid(
      row=0,
      column=5,
      sticky="nsew",
      pady=10,
      padx=5
    )

    self.lectures_count = customtkinter.CTkLabel(search_bar_frame)
    self.lectures_count.grid(
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
