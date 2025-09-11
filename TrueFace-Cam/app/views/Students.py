import sys
import os
import customtkinter

from app.config.context import Context
from app.interfaces.student import Student
from app.config.configrations import Configrations
from app.helper.alerts_manager import AlertsManager
from app.helper.error_handler import error_handler

class Students():
  def __init__(self):
    self._context = Context()
    self._config = Configrations()
    self._alert = AlertsManager()

    self.students_rows = []
    self.headers = [
      "Student ID",
      "First Name",
      "Middle Name",
      "Last Name",
      "Gender"
    ]

  # --------------------
  # operations
  # --------------------

  @error_handler
  def _refresh(self):
    if not self._context.get_current_lecture():
      self._alert.error("Please select a class from the settings")
      return

    self._config.frame_processing_executor.submit(self._display_students_table)

  # --------------------
  # table functions
  # --------------------

  @error_handler
  def _clear_attendance_table(self):
    for widget in self.students_rows:
      widget.destroy()
    self.students_rows.clear()

  @error_handler
  def _add_row(self, student: Student, row):
     for row, student in enumerate(self._context.get_students(), start=1):
        student_row = [
          student.student_id,
          student.first_name,
          student.middle_name,
          student.last_name,
          student.gender
        ]

        for col, data in enumerate(student_row):
          student_data = customtkinter.CTkLabel(
            self.students_table_frame,
            text = data,
            padx = 10,
            pady = 5
          )
          student_data.grid(
            row = row,
            column = col,
            sticky = "nsew"
          )
          self.students_rows.append(student_data)

  @error_handler
  def _display_students_table(self):
    self._clear_attendance_table()

    if len(self._context.get_students()) > 0:
      for row, student in enumerate(self._context.get_students(), start=1):
        self._add_row(student, row)
    else:
      self._alert.error("Please select a lecture from the setting page")

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

    self.students_table_frame = customtkinter.CTkScrollableFrame(parent)
    self.students_table_frame.pack(
      fill = "both",
      expand = True
    )

    for col, header in enumerate(self.headers):
      header_label = customtkinter.CTkLabel(
        self.students_table_frame,
        text = header,
        padx = 10,
        pady = 5
      )
      header_label.grid(
        row = 0,
        column = col,
        sticky = "nsew"
      )

    for col in range(len(self.headers)):
      self.students_table_frame.columnconfigure(
        col,
        weight = 1
      )
    
    self._config.frame_processing_executor.submit(self._display_students_table)