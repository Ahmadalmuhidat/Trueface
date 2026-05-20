import threading
import os

from queue import Queue
from concurrent.futures import ThreadPoolExecutor

class Configurations:
  # singleton pattern
  _instance = None
  _initialized = False

  # static
  window = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    from app.core.face_recognition_module import FaceRecognitionModule
    from app.core.KD_Tree import KD_Tree_Module

    # self._backend_server_ip = "34.29.161.87"
    self._backend_server_ip = "localhost"
    self._backend_port = 8000
    self._backend_entry_route = ""
    self._token = None

    # performance
    self._processing_mode = "CPU"
    cpu_count = os.cpu_count() or 4

    # models
    self.current_recognizer = "face_recognition"
    self.face_recognition_module = FaceRecognitionModule()
    self.KD_tree_module = KD_Tree_Module()

    # thread pools
    self.frame_processing_executor = ThreadPoolExecutor(max_workers=min(cpu_count, 8))
    self.ui_threads_executor = ThreadPoolExecutor(max_workers=2)
    self.shutdown_event = threading.Event()

  def switch_model_to_KTD(self):
    self.KD_tree_module._build_kd_tree()
    self.current_recognizer = "KTD_Tree"

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
    endpoint = f"http://{self._backend_server_ip}:{self._backend_port}"
    if self._backend_entry_route:
      endpoint += f"/{self._backend_entry_route}"
    return endpoint

  @classmethod
  def set_token(cls, token):
    cls()._token = token

  @classmethod
  def get_token(cls):
    return cls()._token

  def get_backend_ip_address(self):
    return self._backend_server_ip

  def set_backend_ip_address(self, ip_address):
    self._backend_server_ip = ip_address

  def get_processing_mode(self):
    return self._processing_mode

  def set_processing_mode(self, mode):
    self._processing_mode = mode