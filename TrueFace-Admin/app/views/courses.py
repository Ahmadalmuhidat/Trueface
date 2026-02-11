import customtkinter
import gc

from app.interfaces.course import Course
from app.config.context import Context
from app.config.configurations import Configurations
from app.config.router import Router
from app.views.course_lectures import Lectures
from app.controllers.courses import CoursesController
from app.utils.error_handler import error_handler
from app.helper.pagination import PaginationComponent

class Courses():
  def __init__(self):
    self._context = Context()
    self._config = Configurations()
    self._router = Router()
    self._courses_controller = CoursesController()

    self.courses = self._context.get_courses()
    self.pagination = None
    self.current_page_data = []
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

  def _search(self, term: str):
    self.courses = [course for course in self._courses if term == course.id or term in course.subject_area]
    self._display_courses_table()

  @error_handler
  def _delete(self, course: Course):
    if self._courses_controller.remove_course(course):
      self._refresh_courses_table()

  @error_handler
  def _create(self):
    new_course = Course(
      self.course_id_entry.get().strip(),
      self.course_title_entry.get().strip(),
      self.course_credit_entry.get().strip(),
      self.course_maximum_units_entry.get().strip(),
      self.course_long_title_entry.get().strip(),
      self.course_offering_nbr_entry.get().strip(),
      self.course_academic_group_entry.get().strip(),
      self.course_subject_area_entry.get().strip(),
      self.course_catalog_nbr_entry.get().strip(),
      self.course_campus_entry.get().strip(),
      self.course_academic_organization_entry.get().strip(),
      self.course_component_entry.get().strip()
    )
    
    if self._courses_controller.add_course(new_course):
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

      self._context.add_course(new_course)
      self.courses.append(new_course)
      
      if self.pagination:
        self.pagination.set_data(self.courses)
      else:
        self._add_course_row(new_course, len(self.courses))
        self.courses_count.configure(text="Results: " + str(len(self.courses)))

  @error_handler
  def _update(self, course: Course):
    course.title = self.course_title_entry.get().strip()
    course.credit = self.course_credit_entry.get().strip()
    course.maximum_units = self.course_maximum_units_entry.get().strip()
    course.long_course_title = self.course_long_title_entry.get().strip()
    course.offering_nbr = self.course_offering_nbr_entry.get().strip()
    course.academic_group = self.course_academic_group_entry.get().strip()
    course.subject_area = self.course_subject_area_entry.get().strip()
    course.catalog_nbr = self.course_catalog_nbr_entry.get().strip()
    course.campus = self.course_campus_entry.get().strip()
    course.academic_organization = self.course_academic_organization_entry.get().strip()
    course.component = self.course_component_entry.get().strip()

    if self._courses_controller.update_course(course):
      self._refresh_courses_table()
      self.pop_window.destroy()

  @error_handler
  def _navigate_to_course_lectures(self, course: Course):
    self._context.set_current_course(course)
    self._router.navigate(Lectures)

  def _on_page_change(self, page_data: list, current_page: int):
    self.current_page_data = page_data
    self._display_courses_table()

  # --------------------
  # forms
  # --------------------
  def _edit_course_form(self, course: Course):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit Course")
    self.pop_window.geometry("500x600")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(450, 500)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    entry_width = 300
    padx, pady = 15, 10

    course_id_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Course ID:"
    )
    course_id_label.grid(
      row=0,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_id_entry.grid(
      row=0,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_id_entry.insert(
      0,
      course.id
    )
    self.course_id_entry.configure(state="readonly")

    course_title_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Title:"
    )
    course_title_label.grid(
      row=1,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_title_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_title_entry.grid(
      row=1,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_title_entry.insert(
      0,
      course.title
    )

    course_credit_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Credit:"
    )
    course_credit_label.grid(
      row=2,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_credit_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_credit_entry.grid(
      row=2,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_credit_entry.insert(
      0,
      course.credit
    )

    course_maximum_units_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Maximum Units:"
    )
    course_maximum_units_label.grid(
      row=3,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_maximum_units_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_maximum_units_entry.grid(
      row=3,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_maximum_units_entry.insert(
      0,
      course.maximum_units
    )

    course_long_title_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Long Course Title:"
    )
    course_long_title_label.grid(
      row=4,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_long_title_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_long_title_entry.grid(
      row=4,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_long_title_entry.insert(
      0,
      course.long_course_title
    )

    course_offering_nbr_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Offering NBR:"
    )
    course_offering_nbr_label.grid(
      row=5,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_offering_nbr_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_offering_nbr_entry.grid(
      row=5,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_offering_nbr_entry.insert(
      0,
      course.offering_nbr
    )

    course_academic_group_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Academic Group:"
    )
    course_academic_group_label.grid(
      row=6,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_academic_group_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_academic_group_entry.grid(
      row=6,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_academic_group_entry.insert(
      0,
      course.academic_group
    )

    course_subject_area_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Subject Area:"
    )
    course_subject_area_label.grid(
      row=7,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_subject_area_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_subject_area_entry.grid(
      row=7,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_subject_area_entry.insert(
      0,
      course.subject_area
    )

    course_catalog_nbr_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Catalog NBR:"
    )
    course_catalog_nbr_label.grid(
      row=8,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_catalog_nbr_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_catalog_nbr_entry.grid(
      row=8,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_catalog_nbr_entry.insert(
      0,
      course.catalog_nbr
    )

    course_campus_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Campus:"
    )
    course_campus_label.grid(
      row=9,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_campus_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_campus_entry.grid(
      row=9,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_campus_entry.insert(
      0,
      course.campus
    )

    course_academic_organization_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Academic Organization:"
    )
    course_academic_organization_label.grid(
      row=10,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_academic_organization_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_academic_organization_entry.grid(
      row=10,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_academic_organization_entry.insert(0, course.academic_organization)

    course_component_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Component:"
    )
    course_component_label.grid(
      row=11,
      column=0,
      padx=padx,
      pady=pady,
      sticky="w"
    )
    self.course_component_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.course_component_entry.grid(
      row=11,
      column=1,
      padx=padx,
      pady=pady
    )
    self.course_component_entry.insert(
      0,
      course.component
    )

    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=11, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Update Course",
      height=35,
      font=("Arial", 12, "bold"),
      command=lambda: self._update(course)
    )
    submit_button.grid(
      row=12,
      column=0,
      columnspan=2,
      padx=padx,
      pady=pady + 10,
      sticky="ew"
    )

    scrollable_frame.columnconfigure(1, weight=1)

  def _add_course_form(self):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New Course")
    self.pop_window.geometry("500x600")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(450, 500)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    entry_w, pad_x, pad_y = 300, 15, 10

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Course ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Title:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_title_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_title_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Credit:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_credit_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_credit_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Maximum Units:",
      anchor="w"
    ).grid(
      row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_maximum_units_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_maximum_units_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Long Course Title:",
      anchor="w"
    ).grid(
      row=4,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_long_title_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_long_title_entry.grid(
      row=4,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Offering NBR:",
      anchor="w"
    ).grid(
      row=5,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_offering_nbr_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_offering_nbr_entry.grid(
      row=5,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Academic Group:",
      anchor="w"
    ).grid(
      row=6,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_academic_group_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_academic_group_entry.grid(
      row=6,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Subject Area:",
      anchor="w"
    ).grid(
      row=7,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_subject_area_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_subject_area_entry.grid(
      row=7,
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
      row=8,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_catalog_nbr_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_catalog_nbr_entry.grid(
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
    self.course_campus_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_campus_entry.grid(
      row=9,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Academic Organization:",
      anchor="w"
    ).grid(
      row=10,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_academic_organization_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_academic_organization_entry.grid(
      row=10,
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
      row=11,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.course_component_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_w
    )
    self.course_component_entry.grid(
      row=11,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=11, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Save Course",
      height=35,
      font=("Arial", 12, "bold"),
      command=self._create
    )
    submit_button.grid(
      row=12,
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
  def _add_course_row(self, course: Course, row: int):
    course_row = [
      course.id,
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
      column=12,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.courses_rows.append(lectures_button)

    edit_button = customtkinter.CTkButton(
      self.courses_table_frame,
      text="Edit",
      command=lambda: self._config.executor.submit(self._edit_course_form, course)
    )
    edit_button.grid(
      row=row,
      column=13,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.courses_rows.append(edit_button)

    delete_button = customtkinter.CTkButton(
      self.courses_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete, course)
    )
    delete_button.grid(
      row=row,
      column=14,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.courses_rows.append(delete_button)

  @error_handler
  def _clear_courses_table(self):
    for widget in self.courses_rows:
      try:
        widget.destroy()
      except:
        pass
    self.courses_rows.clear()
    
    if len(self.courses) > 100:
      gc.collect()

  @error_handler
  def _display_courses_table(self):
    self._clear_courses_table()

    for row, course in enumerate(self.courses, start=1):
      self._add_course_row(course, row)
    
    if self.pagination:
      pagination_info = self.pagination.get_pagination_info()
      self.courses_count.configure(
        text=f"Showing {pagination_info['start_index'] + 1}-{pagination_info['end_index']} of {pagination_info['total_items']} courses"
      )
    else:
      self.courses_count.configure(text="Results: " + str(len(self.courses)))

  def _refresh_courses_table(self):
    self._context.fetch_courses()
    self.courses = self._context.get_courses()

    if self.pagination:
      self.pagination.set_data(self.courses)
    else:
      self._display_courses_table()

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

    self.pagination = PaginationComponent(
      parent=parent,
      items_per_page=10,
      on_page_change=self._on_page_change
    )
    self.pagination.pack(fill="x", pady=(10, 0))
    self.pagination.set_data(self.courses)
