import customtkinter
import tkinter
import gc

from PIL import Image
from app.config.context import Context
from app.config.configurations import Configurations
from app.interfaces.student import Student
from app.config.router import Router
from app.views.student_profile import StudentProfile
from app.controllers.students import StudentsController
from app.utils.error_handler import error_handler
from app.helper.pagination import PaginationComponent
from app.utils.alerts_manager import AlertsManager

class Students:
  def __init__(self):
    self._context = Context()
    self._config = Configurations()
    self._router = Router()
    self._alerts_manager = AlertsManager()
    self._students_controller = StudentsController()

    self.students = self._context.get_students()
    self.pagination = None
    self.current_page_data = []
    self.students_rows = []
    self.headers = [
      "Student ID",
      "First Name",
      "Middle Name",
      "Last Name",
      "Gender",
      "Create Date"
    ]

  # --------------------
  # operations
  # --------------------

  def _search(self, term):
    self.students = [student for student in self._students if term == student.id or term in student.name]
    self._display_students_table()

  @error_handler
  def _delete(self, student: Student):
    if self._students_controller.remove_student(student):
      self._refresh_students_table()

  @error_handler
  def _create(self):
    new_student = Student(
      self.student_id_entry.get().strip(),
      self.student_first_name_entry.get().strip(),
      self.student_middle_name_entry.get().strip(),
      self.student_last_name_entry.get().strip(),
      self.student_gender_entry.get().strip(),
      picture=self.student_image_entry.get().strip()
    )

    if self._students_controller.add_student(new_student):
      for entry in [
        self.student_id_entry,
        self.student_first_name_entry,
        self.student_middle_name_entry,
        self.student_last_name_entry,
        self.student_image_entry
      ]:
        entry.delete(0, customtkinter.END)

      self._context.add_student(new_student)
      self.students.append(new_student)

      if self.pagination:
        self.pagination.set_data(self.students)
      else:
        self._add_student_row(new_student, len(self.students))
        self.students_count.configure(text="Results: " + str(len(self.students)))

  @error_handler
  def _update(self, student: Student):
    student.first_name = self.student_first_name_entry.get()
    student.middle_name = self.student_middle_name_entry.get()
    student.last_name = self.student_last_name_entry.get()
    student.gender = self.student_gender_entry.get()

    if self._students_controller.update_student(student):
      self._refresh_students_table()

  @error_handler
  def _navigate_to_stduent_profile(self, student: Student):
    self._context.set_current_student(student)
    self._router.navigate(StudentProfile)

  def _on_page_change(self, page_data, current_page):
    self.current_page_data = page_data
    self._display_students_table()

  @error_handler
  def _select_image(self):
    file_path = tkinter.filedialog.askopenfilename()
    if file_path:
      image = Image.open(file_path)
      image.thumbnail((150, 150))
      self.student_image = file_path
      self.student_image_entry.delete(0, customtkinter.END)
      self.student_image_entry.insert(0, file_path)

  # --------------------
  # forms
  # --------------------

  def _edit_student_form(self, student: Student):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit Student")
    self.pop_window.geometry("450x450")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(400, 400)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_width = 300
    pad_x, pad_y = 15, 10

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Student ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.student_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.student_id_entry.insert(
      0,
      student.student_id
    )
    self.student_id_entry.configure(state="readonly")

    customtkinter.CTkLabel(
      scrollable_frame,
      text="First Name:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.student_first_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_first_name_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.student_first_name_entry.insert(
      0,
      student.first_name
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Middle Name:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.student_middle_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_middle_name_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.student_middle_name_entry.insert(
      0,
      student.middle_name
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Last Name:",
      anchor="w"
    ).grid(
      row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.student_last_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_last_name_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew")
    self.student_last_name_entry.insert(
      0,
      student.last_name
    )

    customtkinter.CTkLabel(
      scrollable_frame,
      text="Gender:",
      anchor="w"
    ).grid(
      row=4,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.student_gender_entry = customtkinter.CTkComboBox(
      scrollable_frame,
      values=["Male", "Female"],
      width=entry_width
    )
    self.student_gender_entry.grid(
      row=4,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.student_gender_entry.set(student.gender)

    # Add some spacing
    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=5, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Update Student",
      command=lambda: self._update(student),
      height=35,
      font=("Arial", 12, "bold")
    )
    submit_button.grid(
      row=6,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=pad_y + 10,
      sticky="ew"
    )

    # Configure grid weights for responsive layout
    scrollable_frame.columnconfigure(1, weight=1)

  def _add_student_form(self):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New Student")
    self.pop_window.geometry("450x500")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(400, 450)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_width = 300
    pad_x, pad_y = 15, 10

    student_id_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Student ID:",
      anchor="w"
    )
    student_id_label.grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.student_id_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    first_name_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="First Name:",
      anchor="w"
    )
    first_name_label.grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.student_first_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_first_name_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    middle_name_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Middle Name:",
      anchor="w"
    )
    middle_name_label.grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.student_middle_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_middle_name_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    last_name_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Last Name:",
      anchor="w"
    )
    last_name_label.grid(
      row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.student_last_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
      width=entry_width
    )
    self.student_last_name_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    gender_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Gender:",
      anchor="w"
    )
    gender_label.grid(
      row=4,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )
    self.student_gender_entry = customtkinter.CTkComboBox(
      scrollable_frame,
      values=["Male", "Female"],
      width=entry_width
    )
    self.student_gender_entry.set("Male")
    self.student_gender_entry.grid(
      row=4,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    image_label = customtkinter.CTkLabel(
      scrollable_frame,
      text="Image:",
      anchor="w"
    )
    image_label.grid(
      row=5,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    # Create a frame for image selection
    image_frame = customtkinter.CTkFrame(scrollable_frame)
    image_frame.grid(
      row=5,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    
    self.student_image_entry = customtkinter.CTkEntry(
      image_frame,
      placeholder_text="Select an image file"
    )
    self.student_image_entry.pack(
      side="left",
      padx=(0, 10),
      pady=5,
      fill="x",
      expand=True
    )
    
    select_image_button = customtkinter.CTkButton(
      image_frame,
      text="Browse",
      command=self._select_image,
      width=120
    )
    select_image_button.pack(side="right", padx=5, pady=5)

    # Add some spacing
    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(
      row=6,
      column=0,
      columnspan=2,
      pady=10
    )

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Save Student",
      command=self._create,
      height=35,
      font=("Arial", 12, "bold")
    )
    submit_button.grid(
      row=7,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=pad_y + 10,
      sticky="ew"
    )

    # Configure grid weights for responsive layout
    scrollable_frame.columnconfigure(1, weight=1)

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _clear_students_table(self):
    for widget in self.students_rows:
      try:
        widget.destroy()
      except:
        pass
    self.students_rows.clear()
    
    if len(self.students) > 100:
      gc.collect()

  @error_handler
  def _add_student_row(self, student: Student, row):
    student_data = [
      student.student_id,
      student.first_name,
      student.middle_name,
      student.last_name,
      student.gender,
      student.create_date
    ]

    for col, data in enumerate(student_data):
      label = customtkinter.CTkLabel(
        self.students_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      label.grid(row=row, column=col, sticky="nsew")
      self.students_rows.append(label)

    profile_button = customtkinter.CTkButton(
      self.students_table_frame,
      text="Profile",
      command=lambda student=student: self._navigate_to_stduent_profile(student)
    )
    profile_button.grid(
      row=row,
      column=6,
      padx=10,
      pady=5,
      sticky="nsew"
    )
    self.students_rows.append(profile_button)

    edit_button = customtkinter.CTkButton(
      self.students_table_frame,
      text="Edit",
      command=lambda: self._config.executor.submit(self._edit_student_form, student)
    )
    edit_button.grid(
      row=row,
      column=7,
      padx=10,
      pady=5,
      sticky="nsew"
      )
    self.students_rows.append(edit_button)

    delete_button = customtkinter.CTkButton(
      self.students_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete, student)
    )
    delete_button.grid(
      row=row,
      column=8,
      padx=10,
      pady=5,
      sticky="nsew"
      )
    self.students_rows.append(delete_button)

  @error_handler
  def _display_students_table(self):
    self._clear_students_table()

    for row, student in enumerate(self.students, start=1):
      self._add_student_row(student, row)

    if self.pagination:
      pagination_info = self.pagination.get_pagination_info()
      self.students_count.configure(
        text=f"Showing {pagination_info['start_index'] + 1}-{pagination_info['end_index']} of {pagination_info['total_items']} students"
      )
    else:
      self.students_count.configure(text=f"Showing {len(self.students)} students")

  def _refresh_students_table(self):
    self._context.fetch_students()
    self.students = self._context.get_students()

    if self.pagination:
      self.pagination.set_data(self.students)
    else:
      self._display_students_table()

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self, parent: customtkinter.CTkFrame):
    search_bar_frame = customtkinter.CTkFrame(parent, bg_color="transparent")
    search_bar_frame.pack(fill="x", expand=False)

    search_bar = customtkinter.CTkEntry(
      search_bar_frame,
      width=400,
      placeholder_text="Search for Students..."
    )
    search_bar.grid(
      row=0,
      column=1,
      sticky="nsew",
      pady=10
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

    refresh_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._refresh_students_table,
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

    add_student_button = customtkinter.CTkButton(
      search_bar_frame,
      command=self._add_student_form,
      width=100,
      text="Add Student"
    )
    add_student_button.grid(
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

    self.students_table_frame = customtkinter.CTkScrollableFrame(parent)
    self.students_table_frame.pack(fill="both", expand=True)

    for col, header in enumerate(self.headers):
      header_label = customtkinter.CTkLabel(
        self.students_table_frame,
        text=header,
        padx=10,
        pady=10
      )
      header_label.grid(row=0, column=col, sticky="nsew")

    for col in range(len(self.headers)):
      self.students_table_frame.columnconfigure(col, weight=1)

    self.pagination = PaginationComponent(
      parent=parent,
      items_per_page=10,
      on_page_change=self._on_page_change
    )
    self.pagination.pack(fill="x", pady=(10, 0))

    self.pagination.set_data(self.students)

