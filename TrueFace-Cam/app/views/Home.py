import os
import sys
import customtkinter
import psutil
import time
import requests
import json

from app.config.configrations import Configrations
from app.config.context import Context

class Home():
  def __init__(self):
    from app.core.camera_manager import CameraManager

    self._camera_manager = CameraManager()
    self._context = Context()
    self._config = Configrations()

  def update_camera_status(self):
    # check camera status and update label
    if self._camera_manager.camera_scanner.found_active_connected_camera:
      self.camera_status.configure(text="Connected", text_color="green")
    else:
      self.camera_status.configure(text="Disconnected", text_color="red")
    # schedule next update after 5 seconds
    self.window.after(5000, self.update_camera_status)

  def update_api_status(self):
    try:
      response = requests.get(self._config.get_backend_endpoint() + "/").content
      api_active = json.loads(response.decode('utf-8'))
      if api_active.get("data"):
        self.database_status.configure(text="Connected", text_color="green")
      else:
        self.database_status.configure(text="Disconnected", text_color="red")
    except Exception:
      self.database_status.configure(text="Disconnected", text_color="red")
    self.window.after(2000, self.update_api_status)

  def update_cpu_metrics(self):
    metrics = psutil.cpu_percent(interval=None)
    self.cpu_count.configure(text=f"CPU Usage \n\n{metrics}%")
    self.window.after(1000, self.update_cpu_metrics)

  def update_attendance_count(self):
    self.attendance_count.configure(
      text=f"Attendance \n\n{len(self._context.get_attendance())}"
    )
    self.window.after(5000, self.update_attendance_count)

  def launch_view(self, parent):
    try:
      parent.rowconfigure(0, weight = 1)
      parent.rowconfigure(1, weight = 3)
      parent.rowconfigure(2, weight = 1)

      parent.columnconfigure(0, weight = 1)
      parent.columnconfigure(1, weight = 3)
      parent.columnconfigure(2, weight = 1)

      content_frame = customtkinter.CTkFrame(parent)
      content_frame.grid(
        row = 1,
        column = 1,
        sticky = "new"
      )

      content_frame.rowconfigure(0, weight = 1)
      content_frame.rowconfigure(1, weight = 1)

      content_frame.columnconfigure(0, weight = 1)
      content_frame.columnconfigure(1, weight = 1)
      content_frame.columnconfigure(2, weight = 1)
      content_frame.columnconfigure(3, weight = 1)

      capture_button = customtkinter.CTkButton(
        content_frame,
        text = "Start Capture",
        command = self._camera_manager.start_capturing,
        font=customtkinter.CTkFont(size=15)
      )
      capture_button.grid(
        row = 0,
        column = 0,
        columnspan = 2,
        sticky = "nswe"
      )

      stop_capture_button = customtkinter.CTkButton(
        content_frame,
        text = "Stop Capture",
        command = self._camera_manager.stop_capturing,
        height = 50,
        fg_color = "red",
        font = customtkinter.CTkFont(size = 15)
      )
      stop_capture_button.grid(
        row = 0,
        column = 2,
        columnspan = 2,
        sticky = "nswe"
      )

      camera_status_frame = customtkinter.CTkFrame(content_frame, corner_radius = 0)
      camera_status_frame.grid(
        row = 1,
        column = 0,
        sticky = "nsew"
      )
      camera_status_frame.grid_propagate(False)

      self.camera_status_header = customtkinter.CTkLabel(
        camera_status_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Camera Status"
      )
      self.camera_status_header.pack(
        padx = 5,
        pady = 10
      )
      self.camera_status = customtkinter.CTkLabel(camera_status_frame)
      self.camera_status.pack()

      database_status_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      database_status_frame.grid(
        row = 1,
        column = 1,
        sticky = "nsew"
      )
      database_status_frame.grid_propagate(False)

      self.api_status_header = customtkinter.CTkLabel(
        database_status_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "API Status"
      )
      self.api_status_header.pack(
        padx = 5,
        pady = 10
      )

      self.database_status = customtkinter.CTkLabel(database_status_frame)
      self.database_status.pack()

      attendance_count_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      attendance_count_frame.grid(
        row = 1,
        column = 2,
        sticky = "nsew"
      )
      attendance_count_frame.grid_propagate(False)

      self.attendance_count = customtkinter.CTkLabel(
        attendance_count_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Attendance \n\n0"
      )
      self.attendance_count.pack(
        padx = 5,
        pady = 15
      )
      cpu_count_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      cpu_count_frame.grid(
        row = 1,
        column = 3,
        sticky = "nsew"
      )
      cpu_count_frame.grid_propagate(False)

      self.cpu_count = customtkinter.CTkLabel(
        cpu_count_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "CPU Usage \n\n0"
      )
      self.cpu_count.pack(
        padx = 5,
        pady = 15
      )

      self._config.ui_threads_executor.submit(self.update_cpu_metrics)
      self._config.ui_threads_executor.submit(self.update_attendance_count)
      self._config.ui_threads_executor.submit(self.update_api_status)
      self._config.ui_threads_executor.submit(self.update_camera_status)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)  