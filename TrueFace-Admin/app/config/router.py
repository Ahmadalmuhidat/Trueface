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
    self._config = Configurations()

  @error_handler
  def clear_window(self) -> None:
    if self._current_view:
      self._destroy_all_children(self._current_view)
      self._current_view.pack_forget()
      self._current_view.destroy()
      self._current_view = None

  @error_handler
  def _destroy_all_children(self, widget) -> None:
    for child in widget.winfo_children():
      if isinstance(child, customtkinter.CTkFrame):
        self._destroy_all_children(child)
      child.destroy()

  @error_handler
  def navigate(self, view_object) -> None:
    self.clear_window()

    frame = customtkinter.CTkFrame(self._config.get_window())
    view_instance = view_object()
    self._setup_view(frame, view_instance)

  @error_handler
  def _setup_view(self, frame, view_instance) -> None:
    view_instance.launch_view(frame)
    self._current_view = frame
    self._current_view.pack(fill="both", expand=True)
