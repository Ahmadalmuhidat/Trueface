import customtkinter

from app.interfaces.user import User
from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.users import get_users, add_user, remove_user
from app.helper.error_handler import error_handler

class Users():
  def __init__(self):
    self._context = Context()
    self._config = Configrations()

    self.users = self._context.get_users()
    self.users_rows = []
    self.headers = [
      "Users ID",
      "Name",
      "Email",
      "Role",
    ]

  @error_handler
  def _delete(self, user: User):
    self._config.loading_cursor_on()
    remove_user(user)
    self._config.loading_cursor_off()
    self._refresh_users_table()

  def _search(self, term):
    self.users = (filter(term, [user.name for user in self.users]))
    self._display_users_table()

  @error_handler
  def _add_row(self, user: User, row):
    user_row = [
      user.user_id,
      user.name,
      user.email,
      user.role
    ]

    for col, data in enumerate(user_row):
      user_data = customtkinter.CTkLabel(
        self.users_table_frame,
        text=data,
        padx=10,
        pady=5
      )
      user_data.grid(row=row, column=col, sticky="nsew")
      self.users_rows.append(user_data)

    delete_button = customtkinter.CTkButton(
      self.users_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete, user)
    )
    delete_button.grid(
      row=row,
      column=len(user_row),
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.users_rows.append(delete_button)

  @error_handler
  def _clear_users_table(self):
    for widget in self.users_rows:
      widget.destroy()
    self.users_rows.clear()

  @error_handler
  def _display_users_table(self):
    self._config.loading_cursor_on()
    self._clear_users_table()

    for row, user in enumerate(self.users, start=1):
      self._add_row(user, row)

    self.users_count.configure(text="Results: " + str(len(self.users)))
    self._config.loading_cursor_off()

  def _refresh_users_table(self):
    get_users()
    self._display_users_table()

  @error_handler
  def _submit(self):
    self._config.loading_cursor_on()

    new_user = User(
      self.user_id_entry.get(),
      self.user_full_name_entry.get(),
      self.user_email_entry.get(),
      self.user_role_entry.get()
    )
    add_user(new_user)

    self.user_id_entry.delete(0, customtkinter.END)
    self.user_full_name_entry.delete(0, customtkinter.END)
    self.user_email_entry.delete(0, customtkinter.END)

    self._add_row(new_user, len(self.users) + 1)
    self._context.add_user(new_user)
    self.users_count.configure(text="Results: " + str(len(self.users)))
    self._config.loading_cursor_off()

  @error_handler
  def _add_user_pop_window(self):
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
      values=["Admin", "Teacher"],
      width=350
    )
    self.user_role_entry.grid(
      row=4,
      column=1,
      padx=10,
      pady=15
    )
    self.user_role_entry.set("Teacher")

    submit_button = customtkinter.CTkButton(
      self.pop_window,
      text="Save User",
      command=self._submit,
      width=350
    )
    submit_button.grid(
      row=7,
      columnspan=2,
      sticky="nsew",
      padx=10,
      pady=15
    )

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
      text="Search",
      command=lambda: self._search(search_bar.get())
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
      command=self._refresh_users_table,
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
      command=self._add_user_pop_window,
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

    self._config.executor.submit(self._display_users_table)
