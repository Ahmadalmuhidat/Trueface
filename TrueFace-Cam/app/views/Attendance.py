import os
import customtkinter
import pandas

from app.config.context import Context
from app.interfaces.student import Student
from app.config.configurations import Configurations
from app.utils.alerts_manager import AlertsManager
from app.utils.error_handler import error_handler

class Attendance():
  def __init__(self):
    self._context = Context()
    self._config = Configurations()
    self._alert = AlertsManager()
    self._attendance_rows = []
    self._headers = [
      "Student ID",
      "First Name",
      "Middle Name",
      "Last Name",
      "Attended",
      "Attendance Time"
    ]

  # --------------------
  # operations
  # --------------------

  @error_handler
  def _generate_report(self):
    self._config.loading_cursor_on()

    report = pandas.DataFrame(
      [
        [
          attendance.student_id,
          attendance.first_name,
          attendance.middle_name,
          attendance.last_name,
          attendance.is_attended(),
          attendance.time
        ]
        for attendance in self._context.get_students()
      ],
      columns=[
        "Student ID",
        "First Name",
        "Middle Name",
        "Last Name",
        "Attended",
        "Time"
      ]
    )

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_name = "Attendance Report.xlsx"
    file_path = os.path.join(downloads_folder, file_name)
    report.to_excel(
      file_path,
      index = False
    )
    self._alert.success("fyou can find the report in {downloads_folder}")
    self._config.loading_cursor_off()

  @error_handler
  def _refresh(self):
    if not self._context.get_current_lecture():
      self._alert.error("Please select a class from the settings")
      return

    self._config.frame_processing_executor.submit(self._display_attendance_table)

  @error_handler
  def _search(self, term):
    self._config.loading_cursor_on()
    self._display_attendance_table()
    self._config.loading_cursor_off()

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _clear_attendance_table(self):
    for widget in self._attendance_rows:
      widget.destroy()
    self._attendance_rows.clear()

  @error_handler
  def _add_row(self, student: Student, row):
    attendance_row = [
      student.student_id,
      student.first_name,
      student.middle_name,
      student.last_name,
      "Yes" if student.is_attended() else "No",
      student.time
    ]

    for col, data in enumerate(attendance_row):
      attendance_data = customtkinter.CTkLabel(
        self.attendance_table_frame,
        text = data,
        padx = 10,
        pady = 5   
      )
      attendance_data.grid(
        row = row,
        column = col,
        sticky = "nsew"
      )
      self._attendance_rows.append(attendance_data)

  @error_handler
  def _display_attendance_table(self):
    self._clear_attendance_table()

    if len(self._context.get_students()) > 0:
      for row, student in enumerate(self._context.get_students(), start=1):
        self._add_row(student, row)

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self, parent):
    search_bar_frame = customtkinter.CTkFrame(
      parent,
      bg_color = "transparent"
    )
    search_bar_frame.pack(
      fill = "x",
      expand = False
    )

    search_button = customtkinter.CTkButton(
      search_bar_frame,
      command = lambda: self._config.frame_processing_executor.submit(self._search,search_bar.get()),
      text = "Search"
    )
    search_button.grid(
      row = 0,
      column = 0,
      sticky = "nsew",
      pady = 10,
      padx = 5
    )

    search_bar = customtkinter.CTkEntry(
      search_bar_frame,
      width = 400,
      placeholder_text = "Search for Students..."
    )
    search_bar.grid(
      row = 0,
      column = 1,
      sticky = "nsew",
      pady = 10
    )

    refresh_button = customtkinter.CTkButton(
      search_bar_frame,
      command = self._refresh,
      width = 100,
      text = "Refresh"
    )
    refresh_button.grid(
      row = 0,
      column = 2,
      sticky = "nsew",
      pady = 10,
      padx = 5
    )

    report_button = customtkinter.CTkButton(
      search_bar_frame,
      command = self._generate_report,
      width = 100,
      text = "Generate Report"
    )
    report_button.grid(
      row = 0,
      column = 3,
      sticky = "nsew",
      pady = 10,
      padx = 5
    )

    self.attendance_table_frame = customtkinter.CTkScrollableFrame(parent)
    self.attendance_table_frame.pack(
      fill = "both",
      expand = True
    )

    for col, header in enumerate(self._headers):
      header_label = customtkinter.CTkLabel(
        self.attendance_table_frame,
        text = header,
        padx = 10,
        pady = 5   
      )
      header_label.grid(
        row = 0,
        column = col,
        sticky = "nsew"
      )

    for col in range(len(self._headers)):
      self.attendance_table_frame.columnconfigure(
        col,
        weight = 1
      )
    
    self._config.frame_processing_executor.submit(self._display_attendance_table)
