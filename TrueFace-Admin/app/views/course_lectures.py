import customtkinter
import gc

from app.interfaces.lecture import Lecture
from app.config.context import Context
from app.config.configurations import Configurations
from app.interfaces.lecture import Lecture
from app.interfaces.instructor import Instructor
from app.controllers.lectures import LecturesController
from app.utils.error_handler import error_handler
from app.helper.time import convert_to_24h

class Lectures():
  def __init__(self):
    self._context = Context()
    self._config = Configurations()
    self._lectures_controller = LecturesController()

    self.pagination = None
    self.lectures = self._context.get_current_course().get_lectures()
    self.lectures_rows = []
    self.headers = [
      "Lecture ID",
      "Subject",
      "Catalog NBR",	
      "Academic Career",	
      "Course Offering NBR",	
      "Start Time",	
      "End Time",	
      "Section",	
      "Component",	
      "Campus",	
      "Instructor",	
      "Instructor Type"
    ]

  # --------------------
  # operations
  # --------------------

  def _search(self, term: str) -> None:
    self.lectures = self._context.get_current_course().search_lecture(term.strip())
    self._display_lectures_table()

  @error_handler
  def _delete(self, lecture: Lecture):
    if self._lectures_controller.remove_lecture(lecture):
      self._refresh_lectures_table()

  @error_handler
  def _create(self):
    instructor = next((user for user in self._context.get_users() if user.name == self.instructor_id_entry.get()), None)
    instructor = Instructor(
      instructor.user_id,
      instructor.name
    )
    new_lecture = Lecture(
      self.lecture_id_entry.get().strip(),
      self.subject_entry.get().strip(),
      self.catalog_nbr_entry.get().strip(),
      self.academic_career_entry.get().strip(),
      self._context.get_current_course().id,
      self.offering_nbr_entry.get().strip(),
      convert_to_24h(
        self.start_hour_var.get(),
        self.start_minute_var.get(),
        self.start_ampm_var.get()
      ),
      convert_to_24h(
        self.end_hour_var.get(),
        self.end_minute_var.get(),
        self.end_ampm_var.get()
      ),
      self.section_entry.get().strip(),
      self.component_entry.get().strip(),
      self.campus_entry.get().strip(),
      instructor
    )

    if self._lectures_controller.add_lecture(new_lecture):
      self.lecture_id_entry.delete(0, customtkinter.END)
      self.subject_entry.delete(0, customtkinter.END)
      self.catalog_nbr_entry.delete(0, customtkinter.END)
      self.academic_career_entry.delete(0, customtkinter.END)
      self.offering_nbr_entry.delete(0, customtkinter.END)
      self.section_entry.delete(0, customtkinter.END)
      self.component_entry.delete(0, customtkinter.END)
      self.campus_entry.delete(0, customtkinter.END)

      self._context.get_current_course().add_lecture(new_lecture)
      self.lectures.append(new_lecture)
      
      if self.pagination:
        self.pagination.set_data(self.lectures)
      else:
        self._add_lecture_row(new_lecture, len(self.lectures))
        self.lectures_count.configure(text="Results: " + str(len(self.lectures)))

  @error_handler
  def _update(self, lecture: Lecture):
    lecture.subject_area = self.subject_entry.get().strip()
    lecture.catalog_nbr = self.catalog_nbr_entry.get().strip()
    lecture.academic_career = self.academic_career_entry.get().strip()
    lecture.offering_nbr = self.offering_nbr_entry.get().strip()
    lecture.section = self.section_entry.get().strip()
    lecture.component = self.component_entry.get().strip()
    lecture.campus = self.campus_entry.get().strip()

    instructor = next((user for user in self._context.get_users() if user.name == self.instructor_id_entry.get()), None)
    lecture.instructor = Instructor(
      instructor.user_id,
      instructor.name
    )

    if self._lectures_controller.update_lecture(lecture):
      self._refresh_lectures_table()
      self.pop_window.destroy()

  # --------------------
  # forms
  # --------------------

  def _edit_lecture_form(self, lecture: Lecture):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit Lecture")
    self.pop_window.geometry("500x550")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(450, 500)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_w, pad_x, pad_y = 300, 15, 10

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Lecture ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.lecture_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
    customtkinter.CTkLabel(
      scrollable_frame,
      text="Campus:",
      anchor="w"
    ).grid(
      row=7,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.campus_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.campus_entry.grid(
      row=7,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.campus_entry.insert(
      0,
      lecture.campus
    )

    # Instructor
    customtkinter.CTkLabel(
      scrollable_frame,
      text="Instructor:",
      anchor="w"
    ).grid(
      row=8,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.instructor_id_entry = customtkinter.CTkComboBox(
      scrollable_frame,
      width=entry_w,
      values=[u.name for u in self._context.get_users()]
    )
    self.instructor_id_entry.grid(
      row=8,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.instructor_id_entry.set(lecture.instructor.name)

    # Add some spacing
    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(
      row=9,
      column=0,
      columnspan=2,
      pady=10
    )

    # Submit
    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Update Lecture",
      height=35,
      font=("Arial", 12, "bold"),
      command=lambda: self._update(lecture)
    )
    submit_button.grid(
      row=10,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=pad_y + 10,
      sticky="ew"
    )

    # Configure grid weights for responsive layout
    scrollable_frame.columnconfigure(1, weight=1)

  def _add_lecture_form(self):
    self.course_id_title_map = {
      course.title: course.id
      for course in self._context.get_courses()
    }

    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New Lecture")
    self.pop_window.geometry("500x600")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(450, 550)

    # Create a scrollable frame for the form content
    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_w, pad_x, pad_y = 300, 15, 10

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Lecture ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.lecture_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame, values=["AM", "PM"],
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
      text="Instructor:",
      anchor="w"
    ).grid(
      row=10,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.instructor_id_entry = customtkinter.CTkComboBox(
      scrollable_frame,
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

    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=10, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Save Lecture",
      height=35,
      font=("Arial", 12, "bold"),
      command=lambda: self._config.executor.submit(self._create)
    )
    submit_button.grid(
      row=11,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=pad_y + 10,
      sticky="ew"
    )

    scrollable_frame.columnconfigure(1, weight=1)

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _add_lecture_row(self, lecture: Lecture, row: int):
    lecture_row = [
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

    for col, data in enumerate(lecture_row):
      lecture_data = customtkinter.CTkLabel(
        self.lectures_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      lecture_data.grid(row=row, column=col, sticky="nsew")
      self.lectures_rows.append(lecture_data)

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
      command=lambda: self._delete(lecture)
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
      try:
        widget.destroy()
      except:
        pass
    self.lectures_rows.clear()
    
    if len(self.lectures) > 100:
      gc.collect()

  @error_handler
  def _display_lectures_table(self):
    self._clear_lectures_table()

    for row, lecture in enumerate(self.lectures, start=1):
      self._add_lecture_row(lecture, row)

    self.lectures_count.configure(text="Results: " + str(len(self.lectures)))

  def _refresh_lectures_table(self):
    self._context.get_current_course().fetch_lectures()
    self.lectures = self._context.get_current_course().get_lectures()
    self._display_lectures_table()

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
      text="Add Lecture"
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

    self._display_lectures_table()
