import os
import sys

from app.helper.logger import Logger

LOGGER = Logger()

def error_handler(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as e:
      try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb:
          fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
          print(f"Error in {fname}:{exc_tb.tb_lineno} - {exc_type.__name__}: {exc_obj}")
        else:
          print(f"Error: {exc_type.__name__}: {exc_obj}")
        
        LOGGER.log_exception(e)
      except Exception as log_error:
        print(f"Error logging failed: {log_error}")
        print(f"Original error: {e}")
      return None
  return wrapper
import os
import sys
import traceback

from app.helper.logger import Logger

LOGGER = Logger()

def error_handler(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as e:
      tb = e.__traceback__

      while tb.tb_next:
        tb = tb.tb_next

      filename = os.path.basename(tb.tb_frame.f_code.co_filename)
      lineno = tb.tb_lineno

      print(type(e), filename, lineno)
      print(e)

      LOGGER.log_exception(e)
  return wrapper
