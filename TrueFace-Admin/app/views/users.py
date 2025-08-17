import sys
import os
import customtkinter

from app.models import user
from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.users import get_users, search_user, add_user, remove_user

class Users():
  def __init__(self):
    try:
      self.users = []
      self.headers = [
        "Users ID",
        "Name",
        "Email",
        "Role",
      ]
      self.data_manager = Context()
      self._config = Configrations()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def search(self, term):
    try:
      search_user(term)
      self.display_users_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def display_users_table(self):
    try:
      self._config.loading_cursor_on()

      get_users()

      self._config.loading_cursor_off()

      for label in self.users:
        label.destroy()

      if len(self.data_manager.get_users()) > 0:
        for row, user in enumerate(self.data_manager.get_users(), start=1):
          user_row = [
            user.get_user_id(),
            user.get_name(),
            user.get_email(),
            user.get_role()
          ]

          for col, data in enumerate(user_row):
            user_data = customtkinter.CTkLabel(
              self.users_table_frame,
              text=data,
              padx=10,
              pady=5
            )
            user_data.grid(
              row=row,
              column=col,
              sticky="nsew"
            )
            self.users.append(user_data)

            delete_button = customtkinter.CTkButton(
              self.users_table_frame,
                text="Delete",
                fg_color="red",
                command= lambda user_id=user.get_user_id(): self._config.executor(remove_user, user_id, self.refresh_users_table)
              )
            delete_button.grid(
                row=row,
                column=len(user_row),
                sticky="nsew",
                padx=10,
                pady=5
            )
            self.users.append(delete_button)

      self.users_count.configure(
        text="Results: " + str(len(self.data_manager.get_users()))
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def refresh_users_table(self):
    try:
      get_users()
      self.display_users_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def submit_new_user(self):
    try:
      self._config.loading_cursor_on()

      new_user = user.User(
        self.user_id_entry.get(),
        self.user_full_name_entry.get(),
        self.user_email_entry.get(),
        self.user_role_entry.get()
      )

      add_user(new_user)
      
      self.user_id_entry.delete(
        0,
        customtkinter.END
      )
      self.user_full_name_entry.delete(
        0,
        customtkinter.END
      )
      self.user_email_entry.delete(
        0,
        customtkinter.END
      )

      self._config.loading_cursor_off()
      self.refresh_users_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def add_user_pop_window(self):
    try:
      self.pop_window = customtkinter.CTkToplevel()
      self.pop_window.grab_set()

      self.pop_window.geometry("460x350")
      self.pop_window.resizable(False, False)
      self.pop_window.title("Add New User")

      user_id_label = customtkinter.CTkLabel(
        self.pop_window,
        text="User ID:"
      )
      user_id_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=15
      )

      self.user_id_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.user_id_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=15
      )

      user_full_name_label = customtkinter.CTkLabel(
        self.pop_window,
        text="First Name:"
      )
      user_full_name_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=15
      )

      self.user_full_name_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.user_full_name_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=15
      )

      user_email_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Email:"
      )
      user_email_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=15
      )

      self.user_email_entry = customtkinter.CTkEntry(
        self.pop_window,
        width=350
      )
      self.user_email_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=15
      )

      user_password_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Password:"
      )
      user_password_label.grid(
        row=3,
        column=0,
        padx=10,
        pady=15
      )

      user_role_label = customtkinter.CTkLabel(
        self.pop_window,
        text="Role:"
      )
      user_role_label.grid(
        row=4,
        column=0,
        padx=10,
        pady=15
      )

      self.user_role_entry = customtkinter.CTkComboBox(
        self.pop_window,
        values=["admin", "teacher"],
        width=350
      )
      self.user_role_entry.grid(
        row=4,
        column=1,
        padx=10,
        pady=15
      )
      self.user_role_entry.set("teacher")

      submit_button = customtkinter.CTkButton(
        self.pop_window,
        text="Save User",
        command=self.submit_new_user,
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
        text="Search",
        command=lambda: self.search(search_bar.get())
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
        placeholder_text="Search for Users..."
      )
      search_bar.grid(
        row=0,
        column=1,
        sticky="nsew",
        pady=10
      )

      refresh_button = customtkinter.CTkButton(
        search_bar_frame,
        text="Refresh",
        command=self.refresh_users_table,
        width=100
      )
      refresh_button.grid(
        row=0,
        column=4,
        sticky="nsew",
        pady=10,
        padx=5
      )

      add_user_button = customtkinter.CTkButton(
        search_bar_frame,
        text="Add Users",
        command=self.add_user_pop_window,
        width=100
      )
      add_user_button.grid(
        row=0,
        column=5,
        sticky="nsew",
        pady=10,
        padx=5
      )

      self.users_count = customtkinter.CTkLabel(search_bar_frame)
      self.users_count.grid(
        row=0,
        column=6,
        padx=10,
        pady=5
      )

      self.users_table_frame = customtkinter.CTkScrollableFrame(
        parent
      )
      self.users_table_frame.pack(
        fill="both",
        expand=True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          self.users_table_frame,
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
        self.users_table_frame.columnconfigure(col, weight=1)

      self._config.executor.submit(self.display_users_table)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)