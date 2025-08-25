import threading

from concurrent.futures import ThreadPoolExecutor

class Configrations:
  # static
  window = None
  token = None
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    # prevent re-initialization
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # private
    # self._backend_server_ip = "34.29.161.87"
    self._backend_server_ip = "localhost"
    self._backend_port = 8000
    self._backend_entry_route = "admin"

    # threading
    self.executor = ThreadPoolExecutor(max_workers=4)
    self.shutdown_event = threading.Event()
    self.pause_event = threading.Event()
    self.pause_event.set()

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

  @classmethod
  def set_token(cls, token):
    cls.token = token

  @classmethod
  def get_token(cls):
    return cls.token

  def get_backend_endpoint(self):
    return f"http://{self._backend_server_ip}:{self._backend_port}/{self._backend_entry_route}"