import os
import sys

from app.helper.logger import Logger

LOGGER = Logger()

def error_handler(func):
  def wrapper(self, *args, **kwargs):
    try:
      return func(self, *args, **kwargs)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      LOGGER.log_exception(e)
      pass

  return wrapper