import sys
import os
import logging

from logging.handlers import RotatingFileHandler

class Logger:
  def __init__(self, name: str = "Trueface-Cam", log_file: str = "logs/my_app.log", level=logging.INFO, max_bytes=5_000_000, backup_count=3):
    self.logger = logging.getLogger(name)
    self.logger.setLevel(level)
    self.logger.propagate = False
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_format)

    try:
      log_dir = os.path.dirname(log_file)
      if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
      
      file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
      file_handler.setLevel(level)
      file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
      file_handler.setFormatter(file_format)
      
      self.logger.addHandler(file_handler)
    except Exception as e:
      print(f"Warning: Could not create log file {log_file}: {e}")

    self.logger.addHandler(console_handler)

  def log_exception(self, exc: Exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    lineno = exc_tb.tb_lineno
    self.logger.error(f"Exception type: {exc_type.__name__}, File: {filename}, Line: {lineno}, Message: {exc_obj}")
