from CTkMessagebox import CTkMessagebox

class AlertsManager:
  def success(self, message):
    CTkMessagebox(
      title="Success",
      message=message,
      icon="check",
      icon_size=(20, 20)
  )

  def info(self, message):
    CTkMessagebox(
      title="Info",
      message=message,
      icon="info",
      icon_size=(20, 20)
    )

  def error(self, message):
    CTkMessagebox(
      title="Error",
      message=message,
      icon="cancel",
      icon_size=(20, 20)
    )

  def warning(self, message):
    CTkMessagebox(
      title="Warning",
      message=message,
      icon="warning",
      icon_size=(20, 20)
    )
  
  def options(self, message):
    confirmation = CTkMessagebox(
      title = "Confirmation",
      message = message,
      icon = "question",
      icon_size=(20, 20),
      option_1 = "yes",
      option_2 = "cancel" 
    )
    return True if confirmation.get() == "yes" else False
