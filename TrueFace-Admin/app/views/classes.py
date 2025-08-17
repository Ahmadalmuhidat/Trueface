import sys
import os
import customtkinter

from app.models import class_
from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.classes import get_classes, search_class, add_class, remove_class
from app.controllers.courses import get_courses

class Classes():
  def __init__(self):
    try:
      self.classes = []
      self.headers = [
        "Classe ID",
        "Subject",
        "Catalog NBR",	
        "Academic Career",	
        "Course ID",	
        "Course Offering NBR",	
        "Start Time",	
        "End Time",	
        "Section",	
        "Component",	
        "Campus",	
        "Instructor ID",	
        "Instructor Type"
      ]
      self.data_manager = Context()
      self._config = Configrations()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def display_classes_table(self):
    try:
      self._config.loading_cursor_on()

      get_courses()
      get_classes()

      self._config.loading_cursor_off()

      for label in self.classes:
        label.destroy()

      if len(self.data_manager.get_classes()) > 0:
        for row, class_ in enumerate(self.data_manager.get_classes(), start=1):
          class_row = [
            class_.get_class_id(),
            class_.get_subject_area(),
            class_.get_catalog_nbr(),	
            class_.get_academic_career(),	
            class_.get_course(),	
            class_.get_offering_nbr(),	
            class_.get_start_time(),	
            class_.get_end_time(),	
            class_.get_section(),	
            class_.get_component(),	
            class_.get_campus(),	
            class_.get_instructor_id(),	
            class_.get_instructor_type()
          ]

          for col, data in enumerate(class_row):
            class_data = customtkinter.CTkLabel(
              self.classes_table_frame,
              text = data,
              padx = 10,
              pady = 5
            )
            class_data.grid(
              row = row,
              column = col,
              sticky = "nsew"
            )
            self.classes.append(class_data)

            delete_button = customtkinter.CTkButton(
              self.classes_table_frame,
                text = "Delete",
                fg_color = "red",
                command = lambda class_id=class_.get_class_id(): remove_class(class_id, self.refresh_classes_table),
              )
            delete_button.grid(
                row = row,
                column = len(class_row),
                sticky = "nsew",
                padx = 10,
                pady= 5
            )
            self.classes.append(delete_button)

      self.classes_count.configure(
        text="Results: " + str(len(self.data_manager.get_classes()))
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def refresh_classes_table(self):
    try:
      self.display_classes_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def submit_new_class(self):
    try:
      self._config.loading_cursor_on()

      new_class = class_.Class(
        self.class_id_entry.get(),
        self.subject_entry.get(),
        self.catalog_nbr_entry.get(),
        self.academic_career_entry.get(),
        self.course_id_title_map[self.course_id_entry.get()],
        self.offering_nbr_entry.get(),
        self.start_time_entry.get(),
        self.end_time_entry.get(),
        self.section_entry.get(),
        self.component_entry.get(),
        self.campus_entry.get(),
        self.instructor_id_entry.get()
      )

      add_class(new_class)
 
      self.class_id_entry.delete(
        0,
        customtkinter.END
      )
      self.subject_entry.delete(
        0,
        customtkinter.END
      )
      self.catalog_nbr_entry.delete(
        0,
        customtkinter.END
      )
      self.academic_career_entry.delete(
        0,
        customtkinter.END
      )
      self.offering_nbr_entry.delete(
        0,
        customtkinter.END
      )
      self.start_time_entry.delete(
        0,
        customtkinter.END
      )
      self.end_time_entry.delete(
        0,
        customtkinter.END
      )
      self.section_entry.delete(
        0,
        customtkinter.END
      )
      self.component_entry.delete(
        0,
        customtkinter.END
      )
      self.campus_entry.delete(
        0,
        customtkinter.END
      )
      self.instructor_id_entry.delete(
        0,
        customtkinter.END
      )
      self.instructor_type_entry.delete(
        0,
        customtkinter.END
      )

      self._config.loading_cursor_off()
      self.refresh_classes_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def search(self, term: str) -> None:
    try:
      search_class(term)
      self.display_classes_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def add_class_pop_window(self):
    try:
      self.course_id_title_map = {course.get_title(): course.get_course_id() for course in self.data_manager.get_courses()}

      self.pop_window = customtkinter.CTkToplevel()
      self.pop_window.grab_set()

      self.pop_window.geometry("520x550")
      self.pop_window.resizable(False, False)

      self.pop_window.title("Add New Class")

      class_id_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Class ID:"
      )
      class_id_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=5
      )

      self.class_id_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.class_id_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
      )

      subject_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Subject:"
      )
      subject_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=5
      )

      self.subject_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.subject_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
      )

      catalog_nbr_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Catalog NBR:"
      )
      catalog_nbr_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=5
      )

      self.catalog_nbr_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.catalog_nbr_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=5
      )

      academic_career_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Academic Career:"
      )
      academic_career_label.grid(
        row=4,
        column=0,
        padx=10,
        pady=5
      )

      self.academic_career_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.academic_career_entry.grid(
        row=4,
        column=1,
        padx=10,
        pady=5
      )

      offering_nbr_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Course Offering NBR:"
      )
      offering_nbr_label.grid(
        row=5,
        column=0,
        padx=10,
        pady=5
      )

      self.offering_nbr_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.offering_nbr_entry.grid(
        row=5,
        column=1,
        padx=10,
        pady=5
      )

      start_time_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Start Time:"
      )
      start_time_label.grid(
        row=6,
        column=0,
        padx=10,
        pady=5
      )

      self.start_time_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.start_time_entry.grid(
        row=6,
        column=1,
        padx=10,
        pady=5
      )

      end_time_label = customtkinter.CTkLabel(
        self.pop_window,
        text="End Time:"
      )
      end_time_label.grid(
        row=7,
        column=0,
        padx=10,
        pady=5
      )

      self.end_time_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.end_time_entry.grid(
        row=7,
        column=1,
        padx=10,
        pady=5
      )

      section_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Section:"
      )
      section_label.grid(
        row=8,
        column=0,
        padx=10,
        pady=5
      )

      self.section_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.section_entry.grid(
        row=8,
        column=1,
        padx=10,
        pady=5
      )

      component_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Component:"
      )
      component_label.grid(
        row=9,
        column=0,
        padx=10,
        pady=5
      )

      self.component_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.component_entry.grid(
        row=9,
        column=1,
        padx=10,
        pady=5
      )

      campus_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Campus:"
      )
      campus_label.grid(
        row=10,
        column=0,
        padx=10,
        pady=5
      )

      self.campus_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.campus_entry.grid(
        row=10,
        column=1,
        padx=10,
        pady=5
      )

      instructor_id_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Instructor ID:"
      )
      instructor_id_label.grid(
        row=11,
        column=0,
        padx=10,
        pady=5
      )

      self.instructor_id_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.instructor_id_entry.grid(
        row=11,
        column=1,
        padx=10,
        pady=5
      )

      instructor_type_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Instructor Type:"
      )
      instructor_type_label.grid(
        row=12,
        column=0,
        padx=10,
        pady=5
      )

      self.instructor_type_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.instructor_type_entry.grid(
        row=12,
        column=1,
        padx=10,
        pady=5
      )

      course_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Course:"
      )
      course_label.grid(
        row=13,
        column=0,
        padx=10,
        pady=5
      )

      self.course_id_entry = customtkinter.CTkComboBox(
        self.pop_window,
        values=[course.get_title() for course in self.data_manager.get_courses()],
        width=350
      )
      self.course_id_entry.grid(
        row=13,
        column=1,
        padx=10,
        pady=5
      )
      self.course_id_entry.set(self.data_manager.get_courses()[0].get_title())

      submit_button = customtkinter.CTkButton(
        self.pop_window,
        text="Save Class",
        command= lambda _: self._config.executor.submit(self.submit_new_class)
      )
      submit_button.grid(
        row=14,
        columnspan=2,
        sticky="nsew",
        padx=10,
        pady=5
      )

    except Exception as e:
      ExceptionType,ExceptionObject,ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType,FileName,ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def lunch_view(self, parent: customtkinter.CTkFrame):
    try:
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
        command=lambda: self.search(search_bar.get()),
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
        command=self.refresh_classes_table,
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
        command=self.add_class_pop_window,
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

      self.classes_count = customtkinter.CTkLabel(search_bar_frame)
      self.classes_count.grid(
        row=0,
        column=6,
        padx=10,
        pady=5
      )

      self.classes_table_frame = customtkinter.CTkScrollableFrame(parent)
      self.classes_table_frame.pack(
        fill="both",
        expand=True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          self.classes_table_frame,
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
        self.classes_table_frame.columnconfigure(col, weight=1)

      self._config.executor.submit(self.display_classes_table)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)