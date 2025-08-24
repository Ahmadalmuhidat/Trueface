import threading

from concurrent.futures import ThreadPoolExecutor

class Configrations:
  # static
  window = None
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # private
    # self._backend_server_ip = "34.29.161.87"
    self._backend_server_ip = "localhost"
    self._backend_port = 8000
    self._backend_entry_route = "teacher"
    self._processing_mode = "CPU"

    # threading
    self.frame_processing_executor = ThreadPoolExecutor(max_workers=10)
    self.ui_threads_executor = ThreadPoolExecutor(max_workers=5)
    self.shutdown_event = threading.Event()

  @classmethod
  def loading_cursor_on(cls):
    cls.get_window().configure(cursor="watch")
    cls.get_window().update()

  @classmethod
  def loading_cursor_off(cls):
    cls.get_window().configure(cursor="")
    cls.get_window().update()

  @classmethod
  def set_window(cls, window):
    cls.window = window

  @classmethod
  def get_window(cls):
    return cls.window

  def get_backend_endpoint(self):
    return f"http://{self._backend_server_ip}:{self._backend_port}/{self._backend_entry_route}"

  def get_backend_ip_address(self):
    return self._backend_server_ip

  def set_backend_ip_address(self, ip_address):
    self._backend_server_ip = ip_address

  def get_processing_mode(self):
    return self._processing_mode

  def set_processing_mode(self, mode):
    self._processing_mode = mode