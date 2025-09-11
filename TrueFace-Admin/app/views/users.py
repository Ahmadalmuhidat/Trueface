import customtkinter

from app.interfaces.user import User
from app.config.context import Context
from app.config.configrations import Configrations
from app.controllers.users import fetch_users, add_user, remove_user, update_user
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

  # --------------------
  # operations
  # --------------------

  @error_handler
  def _delete_user(self, user: User):
    self._config.loading_cursor_on()
    remove_user(user)
    self.users = self._context.get_users()
    self._refresh_users_table()
    self._config.loading_cursor_off()

  def _search_user(self, term):
    self.users = list(filter(lambda user: term in user.name, self.users))
    self._display_users_table()

  @error_handler
  def _submit_new_user(self):
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
    self.users.append(new_user)
    self.users_count.configure(text="Results: " + str(len(self.users)))
    self._config.loading_cursor_off()

  @error_handler
  def _submit_edit_user(self, user: User):
    self._config.loading_cursor_on()

    user.name = self.user_full_name_entry.get()
    user.email = self.user_email_entry.get()
    user.role = self.user_role_entry.get()

    update_user(user)
    self._refresh_users_table()
    self.pop_window.destroy()
    self._config.loading_cursor_off()

  def _refresh_users_table(self):
    fetch_users()
    self._display_users_table()

  # --------------------
  # forms
  # --------------------

  def _edit_user_form(self, user: User):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit User")
    self.pop_window.geometry("420x300")
    self.pop_window.resizable(False, False)

    entry_width = 300
    padding_x = 15
    padding_y = 10

    customtkinter.CTkLabel(
      self.pop_window,
      text="User ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=padding_x,
      pady=padding_y,
      sticky="w"
    )

    self.user_id_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_id_entry.grid(
      row=0,
      column=1,
      padx=padding_x,
      pady=padding_y,
      sticky="ew"
    )
    self.user_id_entry.insert(0, user.user_id)
    self.user_id_entry.configure(state="readonly")

    customtkinter.CTkLabel(
      self.pop_window,
      text="Full Name:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=padding_x,
      pady=padding_y,
      sticky="w"
    )

    self.user_full_name_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_full_name_entry.grid(
      row=1,
      column=1,
      padx=padding_x,
      pady=padding_y,
      sticky="ew"
    )
    self.user_full_name_entry.insert(0, user.name)

    customtkinter.CTkLabel(
      self.pop_window,
      text="Email:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=padding_x,
      pady=padding_y,
      sticky="w"
    )

    self.user_email_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_email_entry.grid(
      row=2,
      column=1,
      padx=padding_x,
      pady=padding_y,
      sticky="ew"
    )
    self.user_email_entry.insert(0, user.email)

    customtkinter.CTkLabel(
      self.pop_window,
      text="Role:",
      anchor="w"
    ).grid(
      row=3,
      column=0,
      padx=padding_x,
      pady=padding_y,
      sticky="w"
    )

    self.user_role_entry = customtkinter.CTkComboBox(
      self.pop_window,
      values=["Admin", "Teacher"],
      width=entry_width
    )
    self.user_role_entry.grid(
      row=3,
      column=1,
      padx=padding_x, pady=padding_y,
      sticky="ew"
    )
    self.user_role_entry.set(user.role)

    submit_button = customtkinter.CTkButton(
      self.pop_window,
      text="Update User",
      command=lambda: self._submit_edit_user(user),
      width=entry_width
    )
    submit_button.grid(
      row=4,
      column=0,
      columnspan=2,
      padx=padding_x,
      pady=(padding_y + 5),
      sticky="ew"
    )

    self.pop_window.columnconfigure(1, weight=1)

  def _add_user_form(self):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New User")
    self.pop_window.geometry("420x300")
    self.pop_window.resizable(False, False)

    entry_width = 300
    pad_x = 15
    pad_y = 10

    customtkinter.CTkLabel(
      self.pop_window,
      text="User ID:",
      anchor="w"
    ).grid(
      row=0,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_id_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_id_entry.grid(
      row=0,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="First Name:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_full_name_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_full_name_entry.grid(
      row=1,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Email:",
      anchor="w"
    ).grid(
      row=2,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_email_entry = customtkinter.CTkEntry(
      self.pop_window,
      width=entry_width
    )
    self.user_email_entry.grid(
      row=2,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )

    customtkinter.CTkLabel(
      self.pop_window,
      text="Role:",
      anchor="w"
    ).grid(row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_role_entry = customtkinter.CTkComboBox(
      self.pop_window,
      values=["Admin", "Teacher"],
      width=entry_width
    )
    self.user_role_entry.grid(
      row=3,
      column=1,
      padx=pad_x,
      pady=pad_y,
      sticky="ew"
    )
    self.user_role_entry.set("Teacher")

    submit_button = customtkinter.CTkButton(
      self.pop_window,
      text="Save User",
      command=self._submit_new_user,
      width=entry_width
    )
    submit_button.grid(
      row=4,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=(pad_y + 5),
      sticky="ew"
    )

    self.pop_window.columnconfigure(1, weight=1)

  # --------------------
  # table functions
  # --------------------

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

    edit_button = customtkinter.CTkButton(
      self.users_table_frame,
      text="Edit",
      command=lambda: self._config.executor.submit(self._edit_user_form, user)
    )
    edit_button.grid(
      row=row,
      column=4,
      sticky="nsew",
      padx=10,
      pady=5
    )
    self.users_rows.append(edit_button)

    delete_button = customtkinter.CTkButton(
      self.users_table_frame,
      text="Delete",
      fg_color="red",
      command=lambda: self._config.executor.submit(self._delete_user, user)
    )
    delete_button.grid(
      row=row,
      column=5,
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
      text="Search",
      command=lambda: self._search_user(search_bar.get())
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
      command=self._add_user_form,
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