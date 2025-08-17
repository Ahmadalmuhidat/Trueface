from CTkMessagebox import CTkMessagebox

class AlertsManager:
  def pop_window(self, title, message, icon):
    CTkMessagebox(title=title, message=message, icon=icon)
    