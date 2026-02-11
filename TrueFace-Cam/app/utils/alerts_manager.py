from CTkMessagebox import CTkMessagebox

class AlertsManager:
  def success(self, message: str) -> None:
    CTkMessagebox(title="Success", message=message, icon="check")

  def info(self, message: str) -> None:
    CTkMessagebox(title="Info", message=message, icon="info")

  def error(self, message: str) -> None:
    CTkMessagebox(title="Error", message=message, icon="cancel")

  def warning(self, message: str) -> None:
    CTkMessagebox(title="Warning", message=message, icon="warning")
  
  def options(self, message: str) -> bool:
    title = "Confirmation"
    message = message
    icon = "question"
    confirmation = CTkMessagebox(
      title = title,
      message = message,
      icon = icon,
      option_1 = "yes",
      option_2 = "cancel" 
    )
    return True if confirmation.get() == "yes" else False
