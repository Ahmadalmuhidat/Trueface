import os
import sys
import customtkinter
import psutil
import requests
import json

from app.config.configurations import Configurations
from app.config.context import Context
from app.utils.error_handler import error_handler

class Home():
  def __init__(self):
    from app.core.camera_manager import CameraManager

    self._camera_manager = CameraManager()
    self._context = Context()
    self._config = Configurations()
    self._update_timers = {}
    self._last_cpu_metrics = 0
    self._last_attendance_count = 0
    self._destroyed = False

    self.window = None

  # --------------------
  # operations
  # --------------------

  def _schedule_update(self, method_name, delay, *args, **kwargs):
    if self._destroyed or not hasattr(self, 'window') or self.window is None:
      return
    
    if method_name in self._update_timers:
      try:
        self.window.after_cancel(self._update_timers[method_name])
      except:
        pass
      finally:
        del self._update_timers[method_name]
    
    def safe_callback():
      try:
        if hasattr(self, method_name) and callable(getattr(self, method_name)):
          getattr(self, method_name)(*args, **kwargs)
      except Exception as e:
        print(f"Error in scheduled update {method_name}: {e}")
    
    try:
      timer_id = self.window.after(delay, safe_callback)
      self._update_timers[method_name] = timer_id
    except Exception as e:
      print(f"Error scheduling update {method_name}: {e}")

  @error_handler
  def _update_camera_status(self):
    if self._camera_manager.camera_scanner.found_active_connected_camera:
      self.camera_status.configure(
        text="Connected",
        text_color="green"
      )
    else:
      self.camera_status.configure(
        text="Disconnected",
        text_color="red"
      )
    self._schedule_update("_update_camera_status", 5000)

  def _update_api_status(self):
    try:
      response = requests.get(self._config.get_backend_endpoint(), timeout=3).content
      api_active = json.loads(response.decode('utf-8'))

      if api_active.get("data"):
        self.database_status.configure(
          text="Connected",
          text_color="green"
        )
      else:
        self.database_status.configure(
          text="Disconnected",
          text_color="red"
        )

    except Exception:
      self.database_status.configure(
        text="Disconnected",
        text_color="red"
      )
    self._schedule_update("_update_api_status", 3000)

  @error_handler
  def _update_cpu_metrics(self):
    metrics = psutil.cpu_percent(interval=None)
    if abs(metrics - self._last_cpu_metrics) > 2:
      self.cpu_count.configure(text=f"CPU Usage \n\n{metrics}%")
      self._last_cpu_metrics = metrics
    self._schedule_update("_update_cpu_metrics", 2000)

  @error_handler
  def _update_attendance_count(self):
    try:
      students = self._context.get_students()
      if students is None:
        return
      
      current_count = sum(1 for student in students if student.is_attended())
      if current_count != self._last_attendance_count:
        self.attendance_count.configure(text = f"Attendance \n\n{current_count}")
        self._last_attendance_count = current_count
    except Exception as e:
      print(f"Error updating attendance count: {e}")
    finally:
      self._schedule_update("_update_attendance_count", 5000)

  # --------------------
  # view entry
  # --------------------

  @error_handler
  def launch_view(self, parent):
    self.window = parent.winfo_toplevel()
    
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

    try:
      self._config.ui_threads_executor.submit(self._update_cpu_metrics)
      self._config.ui_threads_executor.submit(self._update_attendance_count)
      self._config.ui_threads_executor.submit(self._update_api_status)
      self._config.ui_threads_executor.submit(self._update_camera_status)
    except Exception as e:
      print(f"Error starting UI updates: {e}")
