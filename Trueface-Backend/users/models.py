from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  id = models.CharField(max_length=50, primary_key=True)
  name = models.CharField(max_length=255, db_index=True)
  email = models.EmailField(unique=True, db_index=True)
  role = models.CharField(max_length=50, db_index=True)

  # Set username as nullable/blank so we can use email as the USERNAME_FIELD
  username = models.CharField(max_length=150, unique=True, blank=True, null=True)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["name", "role"]

  class Meta:
    db_table = "Users"
    verbose_name = "User"
    verbose_name_plural = "Users"
    indexes = [
      models.Index(fields=["email"]),
      models.Index(fields=["role"]),
    ]

  def save(self, *args, **kwargs):
    if not self.username:
      self.username = self.email
    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.name} ({self.email})"
