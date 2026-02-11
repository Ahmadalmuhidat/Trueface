import customtkinter
import time
import gc

from app.interfaces.user import User
from app.config.context import Context
from app.config.configurations import Configurations
from app.controllers.users import UsersController
from app.utils.error_handler import error_handler
from app.utils.alerts_manager import AlertsManager

class Users():
  def __init__(self):
    self._context = Context()
    self._config = Configurations()
    self._alerts_manager = AlertsManager()
    self.pagination = None

    self._users_controller = UsersController()
    self.users = self._context.get_users() or []
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
  def _delete(self, user: User):
    self.users = [user for user in self.users if user.id != user.id]
    self._display_users_table()

  @error_handler
  def _create(self):
    new_user = User(
      self.user_id_entry.get().strip(),
      self.user_full_name_entry.get().strip(),
      self.user_email_entry.get().strip(),
      self.user_role_entry.get().strip()
    )
    
    if self._users_controller.add_user(new_user):
      self.user_id_entry.delete(0, customtkinter.END)
      self.user_full_name_entry.delete(0, customtkinter.END)
      self.user_email_entry.delete(0, customtkinter.END)

      self._context.add_user(new_user)
      self.users.append(new_user)
      
      if self.pagination:
        self.pagination.set_data(self.users)
      else:
        self._add_row(new_user, len(self.users))
        self.users_count.configure(text="Results: " + str(len(self.users)))

  @error_handler
  def _update(self, user: User):
    user.name = self.user_full_name_entry.get()
    user.email = self.user_email_entry.get()
    user.role = self.user_role_entry.get()

    if self._users_controller.update_user(user):
      self._refresh_users_table()
      self.pop_window.destroy()

  # --------------------
  # forms
  # --------------------

  def _edit_user_form(self, user: User):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Edit User")
    self.pop_window.geometry("400x350")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(350, 300)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_width = 280
    padding_x = 15
    padding_y = 10

    customtkinter.CTkLabel(
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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

    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=3, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Update User",
      command=lambda: self._update(user),
      height=35,
      font=("Arial", 12, "bold")
    )
    submit_button.grid(
      row=4,
      column=0,
      columnspan=2,
      padx=padding_x,
      pady=(padding_y + 10),
      sticky="ew"
    )

    scrollable_frame.columnconfigure(1, weight=1)

  def _add_user_form(self):
    self.pop_window = customtkinter.CTkToplevel()
    self.pop_window.grab_set()
    self.pop_window.title("Add New User")
    self.pop_window.geometry("400x350")
    self.pop_window.resizable(True, True)
    self.pop_window.minsize(350, 300)

    scrollable_frame = customtkinter.CTkScrollableFrame(self.pop_window)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    entry_width = 280
    pad_x = 15
    pad_y = 10

    customtkinter.CTkLabel(
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
      text="Full Name:",
      anchor="w"
    ).grid(
      row=1,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_full_name_entry = customtkinter.CTkEntry(
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
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
      scrollable_frame,
      text="Role:",
      anchor="w"
    ).grid(row=3,
      column=0,
      padx=pad_x,
      pady=pad_y,
      sticky="w"
    )

    self.user_role_entry = customtkinter.CTkComboBox(
      scrollable_frame,
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

    spacer = customtkinter.CTkLabel(scrollable_frame, text="")
    spacer.grid(row=3, column=0, columnspan=2, pady=10)

    submit_button = customtkinter.CTkButton(
      scrollable_frame,
      text="Save User",
      command=self._create,
      height=35,
      font=("Arial", 12, "bold")
    )
    submit_button.grid(
      row=4,
      column=0,
      columnspan=2,
      padx=pad_x,
      pady=(pad_y + 10),
      sticky="ew"
    )

    scrollable_frame.columnconfigure(1, weight=1)

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
      command=lambda: self._config.executor.submit(self._delete, user)
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
      try:
        widget.destroy()
      except:
        pass
    self.users_rows.clear()
    
    if len(self.users) > 100:
      gc.collect()

  @error_handler
  def _display_users_table(self):
    self._clear_users_table()
    data_to_display = self.users

    for row, user in enumerate(self.users, start=1):
      self._add_row(user, row)

    if self.pagination:
      pagination_info = self.pagination.get_pagination_info()
      self.users_count.configure(
        text=f"Showing {pagination_info['start_index'] + 1}-{pagination_info['end_index']} of {pagination_info['total_items']} users"
      )
    else:
      self.users_count.configure(text=f"Showing {len(self.users)} users")

  def _refresh_users_table(self):
    self._context.fetch_users()
    self.users = self._context.get_users()

    if self.pagination:
      self.pagination.set_data(self.users)
    else:
      self._display_users_table()

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

    self._display_users_table()
