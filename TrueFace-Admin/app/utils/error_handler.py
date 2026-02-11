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
