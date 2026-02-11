import os
import sys
import customtkinter

from app.config.context import Context
from app.controllers.auth import AuthController
from app.utils.error_handler import error_handler

class Login():
  def __init__(self):
    self._context = Context()
    self._auth_controller = AuthController()

  # --------------------
  # operations
  # --------------------

  def _login(self):
    from main import Main

    email = self.email_entry.get()
    password = self.password_entry.get()

    result = self._auth_controller.login(email, password)
    if result:
      self._context.set_jwt_token(result)
      self.window.destroy()
      Main().start_program()

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self):
    self.window = customtkinter.CTk()
    self.window.geometry("400x200")
    self.window.iconbitmap("logo.ico")
    self.window.resizable(
      width = 0,
      height = 0
    )

    self.window.title("Login To TrueFace")

    content_frame = customtkinter.CTkFrame(self.window)
    content_frame.pack(
      padx = 20,
      pady = 20
    )

    email_label = customtkinter.CTkLabel(
      content_frame,
      text = "Email:"
    )
    email_label.grid(
      row = 0,
      column = 0,
      padx = 10,
      pady = 10
    )

    self.email_entry = customtkinter.CTkEntry(
      content_frame,
      width = 250
    )
    self.email_entry.grid(
      row = 0,
      column = 1,
      padx = 10
    )

    password_label = customtkinter.CTkLabel(
      content_frame,
      text = "Password:"
    )
    password_label.grid(
      row = 1,
      column = 0,
      padx = 10,
    )

    self.password_entry = customtkinter.CTkEntry(
      content_frame,
      width = 250,
      show = "*"
    )
    self.password_entry.grid(
      row = 1,
      column = 1,
      padx = 10,
    )

    save_button = customtkinter.CTkButton(
      content_frame,
      text = "Login",
      command = self._login
    )
    save_button.grid(
      row = 6,
      columnspan = 2,
      padx = 10,
      pady = 10,
      sticky = "nsew",
    )

    # --------------------
    # developed by footer
    # --------------------
    footer_label = customtkinter.CTkLabel(
      content_frame,
      text = "Developed by Ahmad Almuhidat",
      font = ("Arial", 10)
    )
    footer_label.grid(
      row = 7,
      columnspan = 2,
      pady = (5, 0)
    )

    self.window.mainloop()
