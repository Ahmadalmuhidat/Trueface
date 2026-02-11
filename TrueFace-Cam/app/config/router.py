import customtkinter

from app.config.configurations import Configurations
from app.utils.error_handler import error_handler

class Router:
  # singleton pattern
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

    self._current_view = None
    self._current_view_instance = None
    self._config = Configurations()

  @error_handler
  def clear_window(self):
    if self._current_view:
      self._current_view.pack_forget()
  
  def get_current_view(self):
    return self._current_view

  @error_handler
  def navigate(self, view_class):
    try:
      self.clear_window()

      frame = customtkinter.CTkFrame(self._config.get_window())
      view_instance = view_class()
      view_instance.launch_view(frame)

      self._current_view = frame
      self._current_view_instance = view_instance
      self._current_view.pack(fill="both", expand=True)

    except Exception as e:
      print(f"Error navigating to view: {e}")
      pass
