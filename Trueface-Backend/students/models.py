from django.db import models


class Student(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  first_name = models.CharField(max_length=255, db_index=True)
  middle_name = models.CharField(max_length=255, blank=True, null=True)
  last_name = models.CharField(max_length=255, db_index=True)
  gender = models.CharField(max_length=10, db_index=True)
  face_id = models.TextField(blank=True, null=True)  # Face encoding data
  create_date = models.DateField(auto_now_add=True, db_index=True)

  class Meta:
    db_table = "Students"
    verbose_name = "Student"
    verbose_name_plural = "Students"
    indexes = [
      models.Index(fields=["first_name", "last_name"]),
      models.Index(fields=["gender"]),
      models.Index(fields=["create_date"]),
    ]

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
