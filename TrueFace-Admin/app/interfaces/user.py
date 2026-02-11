class User:
  def __init__(self, user_id: str, name: str, email: str, role: str) -> None:
    self.user_id = user_id
    self.name = name
    self.email = email
    self.role = role

  def update(self, name: str = None, email: str = None, role: str = None) -> None:
    if name is not None:
      self.name = name
    if email is not None:
      self.email = email
    if role is not None:
      self.role = role
