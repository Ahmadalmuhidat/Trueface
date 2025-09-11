from CTkMessagebox import CTkMessagebox

class AlertsManager:
  def success(self, message):
    CTkMessagebox(title="Success", message=message, icon="check")

  def info(self, message):
    CTkMessagebox(title="Info", message=message, icon="info")

  def error(self, message):
    CTkMessagebox(title="Error", message=message, icon="cancel")

  def warrning(self, message):
    CTkMessagebox(title="Warning", message=message, icon="warrning")
  
  def options(self, message):
    title = "Conformation"
    message = message
    icon = "question"
    conformation = CTkMessagebox(
      title = title,
      message = message,
      icon = icon,
      option_1 = "yes",
      option_2 = "cancel" 
    )
    return True if conformation.get() == "yes" else False