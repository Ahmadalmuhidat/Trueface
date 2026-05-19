from django.db import models

from lecture.models import Lecture
from students.models import Student


class Attendance(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="Student", db_index=True)
  lecture_field = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column="Lecture", db_index=True)
  time = models.TimeField(db_index=True)
  date = models.DateField(db_index=True)

  class Meta:
    db_table = "Attendance"
    verbose_name = "Attendance"
    verbose_name_plural = "Attendance Records"
    unique_together = ["student", "lecture_field", "date"]
    indexes = [
      models.Index(fields=["student"]),
      models.Index(fields=["lecture_field"]),
      models.Index(fields=["date"]),
      models.Index(fields=["lecture_field", "date"]),
      models.Index(fields=["student", "lecture_field"]),
    ]

  def __str__(self):
    return f"{self.student} - {self.lecture_field} on {self.date}"
