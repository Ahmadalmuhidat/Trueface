import sys
import os
import customtkinter
import tkinter
import uuid

from PIL import Image
from app.config.context import Context
from app.config.configrations import Configrations
from app.models import student
from app.controllers.students import get_students, search_student, add_student, remove_student
from app.controllers.classes import add_student_to_class, get_classes_for_selection, get_student_classes, remove_student_from_class, remove_student_from_all_classes

class Students():
  def __init__(self):
    try:
      self.students = []
      self.headers = [
        "Student ID",
        "First Name",
        "Middle Name",
        "Last Name",
        "Gender",
        "Create Date",
      ]
      self.data_manager = Context()
      self._config = Configrations()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def student_classes_window(self, window, navbar, student_id):
    try:
      for widget in window.winfo_children():
        if widget not in (navbar,):
          widget.pack_forget()

      classes = get_student_classes(student_id)
      classes_rows = []
      headers = [
        "Subject",
        "Start Time",    
        "End Time",
        "Day",
        ""
      ]

      # search_bar_frame = customtkinter.CTkFrame(
      #   window,
      #   bg_color="transparent"
      # )
      # search_bar_frame.pack(
      #   fill="x",
      #   expand=False
      # )

      # search_button = customtkinter.CTkButton(
      #   search_bar_frame,
      #   command=lambda: remove_student_from_all_classes(student_id),
      #   text="Clear"
      # )
      # search_button.grid(
      #   row=0,
      #   column=0,
      #   sticky="nsew",
      #   pady=10,
      #   padx=5
      # )
      
      classes_table_frame = customtkinter.CTkScrollableFrame(window)
      classes_table_frame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(headers):
        header_label = customtkinter.CTkLabel(
          classes_table_frame,
          text=header,
          padx=10,
          pady=10
        )
        header_label.grid(
          row=0,
          column=col,
          sticky="nsew"
        )

      for col in range(len(headers)):
        classes_table_frame.columnconfigure(col, weight=1)

      def remove_relation(relation_id):
        try:
          self._config.loading_cursor_on()

          remove_student_from_class(relation_id)
          nonlocal classes
          classes = get_student_classes(student_id)
          display_classes_table()
        
          self._config.loading_cursor_off()

        except Exception as e:
          ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
          FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
          print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
          print(ExceptionObject)
    
      def display_classes_table():
        try:
          self._config.loading_cursor_on()

          for label in classes_rows:
            label.destroy()

          if len(classes) > 0:
            for row, class_ in enumerate(classes, start=1):
              class_row = [
                class_.subject_area,
                class_.start_time,	
                class_.end_time,
                class_.day
              ]

              for col, data in enumerate(class_row):
                class_data = customtkinter.CTkLabel(
                  classes_table_frame,
                  text=data,
                  padx=10,
                  pady=5
                )
                class_data.grid(
                  row=row,
                  column=col,
                  sticky="nsew"
                )
                classes_rows.append(class_data)

              delete_button = customtkinter.CTkButton(
                classes_table_frame,
                text="Remove",
                fg_color="red",
                command= lambda relation_id=class_.relation_id: self._config.executor.submit(remove_relation, relation_id)
              )
              delete_button.grid(
                row=row,
                column=4,
                sticky="nsew",
                padx=10,
                pady=5
              )
              classes_rows.append(delete_button)

          self._config.loading_cursor_off()

        except Exception as e:
          ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
          FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
          print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
          print(ExceptionObject)

      self._config.executor.submit(display_classes_table)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def class_entry_window(self, window, navbar, student_id):
    try:
      classes_for_selection = get_classes_for_selection()
      class_id_title_map = {
        f"{class_.subject_area} {class_.start_time}-{class_.end_time}": class_.class_id for class_ in classes_for_selection
      }

      for widget in window.winfo_children():
        if widget not in (navbar,):
          widget.pack_forget()

      class_label = customtkinter.CTkLabel(
        window,
        text="Select Class:"
      )
      class_label.pack(
        padx=10,
        pady=10
      )

      class_entry = customtkinter.CTkComboBox(
        window,
        values=[f"{class_.subject_area} {class_.start_time}-{class_.end_time}" for class_ in classes_for_selection],
        width=350
      )
      class_entry.pack(
        padx=10,
        pady=10
      )
      class_entry.set("None")

      day_label = customtkinter.CTkLabel(
        window,
        text="Select Day:"
      )
      day_label.pack(
        padx=10,
        pady=10
      )

      day_entry = customtkinter.CTkComboBox(
        window,
        values=[
          "Sunday",
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday"
        ],
        width=350
      )
      day_entry.pack(
        padx=10,
        pady=10
      )
      day_entry.set("None")

      submit_button = customtkinter.CTkButton(
        window,
        text="Save Class",
        command= lambda: self._config.executor.submit(
          add_student_to_class,
          str(uuid.uuid4()),
          student_id,
          class_id_title_map[class_entry.get()],
          day_entry.get())
      )
      submit_button.pack(
        padx=10,
        pady=5
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def student_profile_pop_window(self, student_id, student_name):
    try:
      pop_window = customtkinter.CTkToplevel()
      pop_window.grab_set()

      pop_window.geometry("700x500")
      pop_window.resizable(False, False)
      pop_window.title(f"{student_name} classes")

      navbar = customtkinter.CTkFrame(pop_window)
      navbar.pack(fill = customtkinter.X)

      add_class_button = customtkinter.CTkButton(
        navbar,
        corner_radius=0,
        text="Add Class",
        command=lambda: self.class_entry_window(
          pop_window,
          navbar,
          student_id
        )
      )
      add_class_button.pack(side=customtkinter.LEFT)

      classes_button = customtkinter.CTkButton(
          navbar,
          corner_radius = 0,
          text = "Classes",
          command = lambda: self.student_classes_window(
            pop_window,
            navbar,
            student_id
          )
      )
      classes_button.pack(side=customtkinter.LEFT)

      self.class_entry_window(
        pop_window,
        navbar,
        student_id
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def search(self, term):
    try:
      search_student(term)
      self.display_students_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def display_students_table(self):
    try:
      self._config.loading_cursor_on()

      get_students()

      self._config.loading_cursor_off()

      for label in self.students:
        label.destroy()

      if len(self.data_manager.get_students()) > 0:
        for row, student in enumerate(self.data_manager.get_students(), start=1):
          student_row = [
            student.get_student_id(),
            student.get_first_name(),
            student.get_middle_name(),
            student.get_last_name(),
            student.get_gender(),
            student.get_create_date()
          ]

          for col, data in enumerate(student_row):
            student_data = customtkinter.CTkLabel(
              self.students_table_frame,
              text=data,
              padx=10,
              pady=5
            )
            student_data.grid(
              row=row,
              column=col,
              sticky="nsew"
            )

            self.students.append(student_data)

          profile_button = customtkinter.CTkButton(
            self.students_table_frame,
            text="Profile",
            command=lambda student_id=student.get_student_id(), student_name=f"{student.get_first_name()} {student.get_middle_name()} {student.get_last_name()}": self.student_profile_pop_window(student_id, student_name)
          )
          profile_button.grid(
            row=row,
            column=6,
            padx=10,
            pady=5,
            sticky="nsew"
          )
          self.students.append(profile_button)

          delete_button = customtkinter.CTkButton(
            self.students_table_frame,
              text = "Delete",
              fg_color = "red",
              command = lambda student_id=student.get_student_id(): remove_student(student_id, self.refresh_students_table)
            )
          delete_button.grid(
            row = row,
            column = 7,
            sticky = "nsew",
            padx = 10,
            pady= 5
          )
          self.students.append(delete_button)

      self.students_count.configure(text="Results: " + str(len(self.data_manager.get_students())))

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def refresh_students_table(self):
    try:
      get_students()
      self.display_students_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def select_image(self):
    try:
      file_path = tkinter.filedialog.askopenfilename()

      if file_path:
        image = Image.open(file_path)
        image.thumbnail((150, 150))
        self.student_image = file_path
        self.student_image_entry.delete(0, customtkinter.END)
        self.student_image_entry.insert(0, file_path)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def submit_new_student(self):
    try:
      self._config.loading_cursor_on()

      new_student = student.Student(
        self.student_id_entry.get(),
        self.student_first_name_entry.get(),
        self.student_middle_name_entry.get(),
        self.student_last_name_entry.get(),
        self.student_gender_entry.get(),
        picture= self.student_image_entry.get()
      )

      add_student(new_student)

      self.student_id_entry.delete(
        0,
        customtkinter.END
      )
      self.student_first_name_entry.delete(
        0,
        customtkinter.END
      )
      self.student_middle_name_entry.delete(
        0,
        customtkinter.END
      )
      self.student_last_name_entry.delete(
        0,
        customtkinter.END
      )
      self.student_image_entry.delete(
        0,
        customtkinter.END
      )

      self._config.loading_cursor_on()
      self.refresh_students_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def add_student_pop_window(self):
    try:
      self.pop_window = customtkinter.CTkToplevel()
      self.pop_window.grab_set()
      self.pop_window.geometry("490x410")
      self.pop_window.resizable(False, False)
      self.pop_window.title("Add New Student")

      student_id_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Student ID:"
      )
      student_id_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=15
      )

      self.student_id_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.student_id_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=15
      )

      student_first_name_label = customtkinter.CTkLabel(
        self.pop_window,
        text="First Name:"
      )
      student_first_name_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=15
      )

      self.student_first_name_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.student_first_name_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=15
      )

      student_middle_name_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Middle Name:"
      )
      student_middle_name_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=15
      )

      self.student_middle_name_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.student_middle_name_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=15
      )

      student_last_name_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Last Name:"
      )
      student_last_name_label.grid(
        row=3,
        column=0,
        padx=10,
        pady=15
      )

      self.student_last_name_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.student_last_name_entry.grid(
        row=3,
        column=1,
        padx=10,
        pady=15
      )

      student_gender_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Gender:"
      )
      student_gender_label.grid(
        row=4,
        column=0,
        padx=10,
        pady=15
      )

      self.student_gender_entry = customtkinter.CTkComboBox(
        self.pop_window,
        values=["Male", "Female"],
        width=350
      )
      self.student_gender_entry.grid(
        row=4,
        column=1,
        padx=10,
        pady=15
      )
      self.student_gender_entry.set("Male")

      self.student_image_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.student_image_entry.grid(
        row=5,
        column=1,
        padx=10,
        pady=15
      )

      select_image_button = customtkinter.CTkButton(
        self.pop_window,
        text="Select Image",
        width=30,
        height=30,
        command=self.select_image
      )
      select_image_button.grid(
        row=5,
        column=0,
        padx=10,
        pady=15
      )

      submit_button = customtkinter.CTkButton(
        self.pop_window,
        text="Save Students",
        command=self.submit_new_student,
        width=350
      )
      submit_button.grid(
        row=7,
        columnspan=2,
        sticky="nsew",
        padx=10,
        pady=15
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
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
        placeholder_text="Search for Students..."
      )
      search_bar.grid(
        row=0,
        column=1,
        sticky="nsew",
        pady=10
      )

      refresh_button = customtkinter.CTkButton(
        search_bar_frame,
        command=self.refresh_students_table,
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
        command=self.add_student_pop_window,
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
      self.students_table_frame.pack(
        fill="both",
        expand=True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          self.students_table_frame,
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
        self.students_table_frame.columnconfigure(col, weight=1)

      self._config.executor.submit(self.display_students_table)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)()