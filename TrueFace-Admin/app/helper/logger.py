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

    os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(level)
    file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    file_handler.setFormatter(file_format)

    self.logger.addHandler(console_handler)
    self.logger.addHandler(file_handler)

  def log_exception(self, exc: Exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    lineno = exc_tb.tb_lineno
    self.logger.error(f"Exception type: {exc_type.__name__}, File: {filename}, Line: {lineno}, Message: {exc_obj}")