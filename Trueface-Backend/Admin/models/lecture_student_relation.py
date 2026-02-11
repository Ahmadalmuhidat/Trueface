from django.db import models
from .student import Student
from .lecture import Lecture

class LectureStudentRelation(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='Student', db_index=True)
  lecture_field = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='Lecture', db_index=True)
  day = models.CharField(max_length=20, db_index=True)  # Day of the week
  
  class Meta:
    db_table = 'LectureStudentRelation'
    verbose_name = 'Lecture Student Relation'
    verbose_name_plural = 'Lecture Student Relations'
    unique_together = ['student', 'lecture_field', 'day']
    indexes = [
      models.Index(fields=['student']),
      models.Index(fields=['lecture_field']),
      models.Index(fields=['day']),
      models.Index(fields=['lecture_field', 'day']),
    ]

  def __str__(self):
    return f"{self.student} - {self.lecture_field} ({self.day})"