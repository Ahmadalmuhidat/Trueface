import os
import sys
import customtkinter

from app.config.configrations import Configrations
from app.helper.logger import Logger

class Router:
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # private
    self._current_view = None
    self._config = Configrations()
    self._logger = Logger()

  def clear_window(self):
    if self._current_view:
      self._current_view.pack_forget()
  
  def get_current_view(self):
    return self._current_view
  
  def navigate(self, view_class):
    try:
      self.clear_window()

      frame = customtkinter.CTkFrame(self._config.get_window())
      view_instance = view_class()
      view_instance.launch_view(frame)

      self._current_view = frame
      self._current_view.pack(fill="both", expand=True)

    except Exception as e:
      self._logger.log_exception(e)
      pass