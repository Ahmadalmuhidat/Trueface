import customtkinter

from app.interfaces.course import Course
from app.config.context import Context
from app.config.configrations import Configrations
from app.config.router import Router
from app.views.course_lectures import Lectures
from app.controllers.courses import add_course, remove_course, get_courses
from app.helper.error_handler import error_handler

class Courses():
  def __init__(self):
    self._context = Context()
    self._config = Configrations()
    self._router = Router()

    self.courses = self._context.get_courses()
    self.courses_rows = []
    self.headers = [
      "Course ID",
      "Course Title",
      "Course Credit",
      "Maximum Units",
      "Long Course Title",
      "Offering NBR",
      "Academic Group",
      "Subject Area",
      "Catalog NBR",
      "Campus",
      "Academic Organization",
      "Component",
      "",
      ""
    ]

  # --------------------
  # operations
  # --------------------

  def _search_course(self, term):
    self.courses = list(filter(lambda c: term in c.subject_area, self._context.get_courses()))
    self._display_courses_table()

  @error_handler
  def _delete_course(self, course: Course):
    self._config.loading_cursor_on()
    remove_course(course)
    self.courses = self._context.get_courses()
    self._config.loading_cursor_on()
    self._display_courses_table()

  def _refresh_courses_table(self):
    get_courses()
    self._display_courses_table()

  @error_handler
  def _submit_new_course(self):
    self._config.loading_cursor_on()

    new_course = Course(
      self.course_id_entry.get(),
      self.course_title_entry.get(),
      self.course_credit_entry.get(),
      self.course_maximum_units_entry.get(),
      self.course_long_title_entry.get(),
      self.course_offering_nbr_entry.get(),
      self.course_academic_group_entry.get(),
      self.course_subject_area_entry.get(),
      self.course_catalog_nbr_entry.get(),
      self.course_campus_entry.get(),
      self.course_academic_organization_entry.get(),
      self.course_component_entry.get()
    )
    add_course(new_course)

    self.course_id_entry.delete(0, customtkinter.END)
    self.course_title_entry.delete(0, customtkinter.END)
    self.course_credit_entry.delete(0, customtkinter.END)
    self.course_maximum_units_entry.delete(0, customtkinter.END)
    self.course_long_title_entry.delete(0, customtkinter.END)
    self.course_offering_nbr_entry.delete(0, customtkinter.END)
    self.course_academic_group_entry.delete(0, customtkinter.END)
    self.course_subject_area_entry.delete(0, customtkinter.END)
    self.course_catalog_nbr_entry.delete(0, customtkinter.END)
    self.course_campus_entry.delete(0, customtkinter.END)
    self.course_academic_organization_entry.delete(0, customtkinter.END)
    self.course_component_entry.delete(0, customtkinter.END)

    self._add_row(new_course, len(self.courses) + 1)
    self._context.add_course(new_course)
    self.courses.append(new_course)
    self.courses_count.configure(text="Results: " + str(len(self.courses)))
    self._config.loading_cursor_off()

  @error_handler
  def _navigate_to_course_lectures(self, course: Course):
    self._context.set_current_course(course)
    self._router.navigate(Lectures)

  # --------------------
  # forms
  # --------------------

  @error_handler
  def _add_course_form(self):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()

    self.pop_window.geometry("535x510")
    self.pop_window.resizable(False, False)

    self.pop_window.title("Add New Course")

    course_id_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Course ID:"
    )
    course_id_label.grid(
      row=0,
      column=0,
      padx=10,
      pady=5
    )
    self.course_id_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_id_entry.grid(
      row=0,
      column=1,
      padx=10,
      pady=5
    )

    course_title_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Title:"
    )
    course_title_label.grid(
      row=1, 
      column=0,
      padx=10,
      pady=5
    )
    self.course_title_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_title_entry.grid(
      row=1, 
      column=1, 
      padx=10, 
      pady=5
    )

    course_credit_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Credit:"
    )
    course_credit_label.grid(
      row=2,
      column=0,
      padx=10,
      pady=5
    )

    self.course_credit_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_credit_entry.grid(
      row=2,
      column=1,
      padx=10,
      pady=5
    )

    course_maximum_units_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Maximum Units:"
    )
    course_maximum_units_label.grid(
      row=3,
      column=0,
      padx=10,
      pady=5
    )

    self.course_maximum_units_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_maximum_units_entry.grid(
      row=3,
      column=1,
      padx=10,
      pady=5
    )

    course_long_title_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Long Course Title:"
    )
    course_long_title_label.grid(
      row=4,
      column=0,
      padx=10,
      pady=5
    )

    self.course_long_title_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_long_title_entry.grid(
      row=4,
      column=1,
      padx=10,
      pady=5
    )

    course_offering_nbr_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Offering NBR:"
    )
    course_offering_nbr_label.grid(
      row=5,
      column=0,
      padx=10,
      pady=5
    )

    self.course_offering_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_offering_nbr_entry.grid(
      row=5,
      column=1,
      padx=10,
      pady=5
    )

    course_academic_group_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Academic Group:"
    )
    course_academic_group_label.grid(
      row=6,
      column=0,
      padx=10,
      pady=5
    )

    self.course_academic_group_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_academic_group_entry.grid(
      row=6,
      column=1,
      padx=10,
      pady=5
    )

    course_subject_area_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Subject Area:"
    )
    course_subject_area_label.grid(
      row=7,
      column=0,
      padx=10,
      pady=5
    )

    self.course_subject_area_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_subject_area_entry.grid(
      row=7,
      column=1,
      padx=10,
      pady=5
    )

    course_catalog_nbr_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Catalog NBR:"
    )
    course_catalog_nbr_label.grid(
      row=8,
      column=0,
      padx=10,
      pady=5
    )

    self.course_catalog_nbr_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_catalog_nbr_entry.grid(
      row=8,
      column=1,
      padx=10,
      pady=5
    )

    course_campus_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Campus:"
    )
    course_campus_label.grid(
      row=9,
      column=0,
      padx=10,
      pady=5
    )

    self.course_campus_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_campus_entry.grid(
      row=9,
      column=1,
      padx=10,
      pady=5
    )

    course_academic_organization_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Academic Organization:"
    )
    course_academic_organization_label.grid(
      row=10,
      column=0,
      padx=10,
      pady=5
    )

    self.course_academic_organization_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_academic_organization_entry.grid(
      row=10,
      column=1,
      padx=10,
      pady=5
    )

    course_component_label = customtkinter.CTkLabel(
      self.pop_window,
      text="Component:"
    )
    course_component_label.grid(
      row=11,
      column=0,
      padx=10,
      pady=5
    )

    self.course_component_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=350
    )
    self.course_component_entry.grid(
      row=11,
      column=1,
      padx=10,
      pady=5
    )

    submit_button = customtkinter.CTkButton(
      self.pop_window,
      text="Save Course",
      command=self._submit_new_course,
      width=350
    )
    submit_button.grid(
      row=12,
      columnspan=2,
      sticky="nsew",
      padx=10,
      pady=5
    )

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _add_row(self, course: Course, row):
    course_row = [
      course.course_id,
      course.title,
      course.credit,
      course.maximum_units,
      course.long_course_title,
      course.offering_nbr,
      course.academic_group,
      course.subject_area,
      course.catalog_nbr,
      course.campus,
      course.academic_organization,
      course.component
    ]

    for col, data in enumerate(course_row):
      course_data = customtkinter.CTkLabel(
        self.courses_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      course_data.grid(row=row, column=col, sticky="nsew")
      self.courses_rows.append(course_data)

    lectures_button = customtkinter.CTkButton(
      self.courses_table_frame,
      text="Lectures",
      command=lambda course=course: self._navigate_to_course_lectures(course)
    )
    lectures_button.grid(
      row=row,
      column=len(course_row),
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.courses_rows.append(lectures_button)

    delete_button = customtkinter.CTkButton(
      self.courses_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete_course, course)
    )
    delete_button.grid(
      row=row,
      column=len(course_row)+1,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.courses_rows.append(delete_button)

  @error_handler
  def _clear_courses_table(self):
    for widget in self.courses_rows:
      widget.destroy()
    self.courses_rows.clear()

  @error_handler
  def _display_courses_table(self):
    self._config.loading_cursor_on()
    self._clear_courses_table()

    for row, course in enumerate(self.courses, start=1):
      self._add_row(course, row)

    self.courses_count.configure(text="Results: " + str(len(self.courses)))
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
      command=lambda: self._search_course(search_bar.get()),
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
      placeholder_text="Search for Courses..."
    )
    search_bar.grid(
      row=0,
      column=1,
      sticky="nsew",
      pady=10
    )

    refersh_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._refresh_courses_table,
      width=100,
      text="Refresh"
    )
    refersh_button.grid(
      row=0,
      column=4,
      sticky="nsew",
      pady=10,
      padx=5
    )

    add_course_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._add_course_form,
      width=100,
      text="Add Course"
    )
    add_course_button.grid(
      row=0,
      column=5,
      sticky="nsew",
      pady=10,
      padx=5
    )

    self.courses_count = customtkinter.CTkLabel(
      search_bar_frame
    )
    self.courses_count.grid(
      row=0,
      column=6,
      padx=10,
      pady=5
    )

    self.courses_table_frame = customtkinter.CTkScrollableFrame(parent)
    self.courses_table_frame.pack(
      fill="both",
      expand=True
    )

    for col, header in enumerate(self.headers):
      header_label = customtkinter.CTkLabel(
        self.courses_table_frame,
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
      self.courses_table_frame.columnconfigure(col, weight=1)

    self._config.executor.submit(self._display_courses_table)
