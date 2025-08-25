import customtkinter

from app.config.configrations import Configrations

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

  def clear_window(self):
    if self._current_view:
      self._current_view.pack_forget()
  
  def get_current_page(self):
    return self._current_view
  
  def get_router_configrations(self):
    return self._config

  def navigate(self, view_object):
    self.clear_window()

    frame = customtkinter.CTkFrame(self._config.get_window())
    view_instance = view_object()

    view_instance.launch_view(frame)

    self._current_view = frame
    self._current_view.pack(fill="both", expand=True)