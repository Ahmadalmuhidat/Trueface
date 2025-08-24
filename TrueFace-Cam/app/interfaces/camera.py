import cv2

from app.helper.logger import Logger

class Camera:
  def __init__(self, index, name):
    self._name = name
    self._index = index
    self._logger = Logger()
  
  def get_name(self):
    return self._name
  
  def get_index(self):
    return self._index
  
  def test_if_working(self):
    try:
      camera = cv2.VideoCapture(self._index)

      if camera.isOpened():
        is_reading, frame = camera.read()

        if is_reading:
          camera.release() 
          cv2.destroyAllWindows()
          return True
      return False

    except Exception as e:
      self._logger.log_exception(e)
      pass

  def view_stream(self):
    try:
      cap = cv2.VideoCapture(self._index)
      WindowTitle = "Camera View"

      while True:
        is_reading, frame = cap.read()

        if is_reading:
          cv2.imshow(WindowTitle, frame)
          UserQuit = cv2.waitKey(1) & 0xFF == ord('q')
          UserClosedWindow = cv2.getWindowProperty(WindowTitle, cv2.WND_PROP_VISIBLE) < 1

          if UserQuit or UserClosedWindow: 
            break

      cap.release() 
      cv2.destroyAllWindows()

    except Exception as e:
      self._logger.log_exception(e)
      pass