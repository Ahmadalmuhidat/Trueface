import threading
import os

from concurrent.futures import ThreadPoolExecutor

class Configurations:
  # singleton pattern
  _instance = None
  _initialized = False

  # static
  window = None
  token = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # private
    self._backend_server_ip = "localhost"
    self._backend_port = 8000
    self._backend_entry_route = ""

    # public
    self.executor = ThreadPoolExecutor(
      max_workers=min(8, (os.cpu_count() or 1) + 4),
      thread_name_prefix="TrueFace"
    )
    self.shutdown_event = threading.Event()
    self.pause_event = threading.Event()
    self.pause_event.set()

  @classmethod
  def loading_cursor_on(cls) -> None:
    cls.get_window().configure(cursor="wait")
    cls.get_window().update()

  @classmethod
  def loading_cursor_off(cls) -> None:
    cls.get_window().configure(cursor="")
    cls.get_window().update()
  @classmethod
  def set_window(cls, window) -> None:
    cls.window = window

  @classmethod
  def get_window(cls) -> None:
    return cls.window

  @classmethod
  def set_token(cls, token) -> None:
    cls.token = token

  @classmethod
  def get_token(cls) -> str:
    return cls.token

  def get_backend_endpoint(self):
    base_url = f"http://{self._backend_server_ip}:{self._backend_port}"
    if self._backend_entry_route:
      return f"{base_url}/{self._backend_entry_route}"
    return base_url
