import sys
import os
import customtkinter

from app.config.context import Context
from app.config.configrations import Configrations
from app.helper.alerts_manager import AlertsManager

class Students():
  def __init__(self):
    self._context = Context()
    self._config = Configrations()
    self._alert = AlertsManager()

    self.students = []
    self.headers = [
      "Student ID",
      "First Name",
      "Middle Name",
      "Last Name",
      "Gender"
    ]

  def _display_students_table(self):
    try:
      for label in self.students:
        label.destroy()

      if len(self._context.get_students()) > 0:
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
            self.students.append(student_data)
      else:
        self._alert.pop_window(
          "No Student Available",
          "Please select a lecture from the setting page",
          "cancel"
        )
  
    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def _refresh(self):
    try:
      if not self._context.get_current_lecture():
          self._alert.pop_window(
            "Error",
            "Please select a class from the settings",
            "cancel"
          )
          return

      self._config.frame_processing_executor.submit(self._display_students_table)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def launch_view(self, parent):
    try:
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

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)