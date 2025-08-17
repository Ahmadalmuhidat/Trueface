import os
import sys
import customtkinter

from app.config.configrations import Configrations
from app.core.logger import Logger

class Router:
  def __init__(self):
    # private
    self._current_page = None
    self._config = Configrations()
    self._logger = Logger()

  def clear_window(self):
    if self._current_page:
      self._current_page.pack_forget()
  
  def get_current_page(self):
    return self._current_page
  
  def get_router_configrations(self):
    return self._config

  def navigate(self, view_class):
    try:
      self.clear_window()

      frame = customtkinter.CTkFrame(self._config.get_window())
      view_instance = view_class()
      view_instance.launch_view(frame)

      self._current_page = frame
      self._current_page.pack(fill="both", expand=True)

    except Exception as e:
      self._logger.log_exception(e)
      pass