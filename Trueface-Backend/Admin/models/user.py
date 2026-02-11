from django.db import models

class User(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  name = models.CharField(max_length=255, db_index=True)
  email = models.EmailField(unique=True, db_index=True)
  password = models.CharField(max_length=255)
  role = models.CharField(max_length=50, db_index=True)
  
  class Meta:
    db_table = 'Users'
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    indexes = [
      models.Index(fields=['email']),
      models.Index(fields=['role']),
    ]
  
  def __str__(self):
    return f"{self.name} ({self.email})"
