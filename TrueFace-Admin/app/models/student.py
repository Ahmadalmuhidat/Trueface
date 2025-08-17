import sys
import os
import requests
import json
import base64
import face_recognition
import pickle
import app.config.configrations as Configrations

from CTkMessagebox import CTkMessagebox

class Student:
  def __init__(self, student_id, first_name, middle_name, last_name, gender, create_date = None, picture = None):
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = gender
    self.create_date = create_date
    self.picture = picture

    self.config  = Configrations.Configrations()
    self.classes = []
  
  def get_student_id(self):
    return self.student_id

  def get_first_name(self):
    return self.first_name

  def get_middle_name(self):
    return self.middle_name

  def get_last_name(self):
    return self.last_name

  def get_gender(self):
    return self.gender

  def get_create_date(self):
    return self.create_date

  def get_picture(self):
    return self.picture

  def get_config(self):
    return self.config

  def get_classes(self):
    return self.classes

  def check_duplicated_id(self):
    try:
      data = {
        "student_id": self.student_id
      }
      response = requests.get(
        self.config.get_base_url() + "/check_duplicated_id",
        params = data,
			  timeout=20
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        return response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while checking duplicated IDs",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass
  
  def get_face_encode(self):
    try:
      load_stored_image = face_recognition.load_image_file(self.picture)
      return base64.b64encode(pickle.dumps(face_recognition.face_encodings(load_stored_image)[0])).decode('utf-8')

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def check_face_in_image(self):
    try:
      load_stored_image = face_recognition.load_image_file(self.picture)
      face_found = face_recognition.face_locations(load_stored_image)

      if face_found:
        return True
      else:
        return False

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass