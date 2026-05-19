from django.db import models

from course.models import Course
from students.models import Student
from users.models import User


class Lecture(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  subject_area = models.CharField(max_length=100, db_index=True)
  catalog_nbr = models.CharField(max_length=50, db_index=True)
  academic_career = models.CharField(max_length=50)
  course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="Course", db_index=True)
  offering_nbr = models.CharField(max_length=50)
  start_time = models.TimeField(db_index=True)
  end_time = models.TimeField(db_index=True)
  section = models.CharField(max_length=50)
  component = models.CharField(max_length=50)
  campus = models.CharField(max_length=100)
  instructor = models.ForeignKey(User, on_delete=models.CASCADE, db_column="Instructor", db_index=True)

  class Meta:
    db_table = "Lectures"
    verbose_name = "Lecture"
    verbose_name_plural = "Lectures"
    indexes = [
      models.Index(fields=["course"]),
      models.Index(fields=["instructor"]),
      models.Index(fields=["subject_area", "catalog_nbr"]),
      models.Index(fields=["start_time", "end_time"]),
    ]

  def __str__(self):
    return f"{self.subject_area} {self.catalog_nbr} - {self.section}"


class LectureStudentRelation(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="Student", db_index=True)
  lecture_field = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column="Lecture", db_index=True)
  day = models.CharField(max_length=20, db_index=True)  # Day of the week

  class Meta:
    db_table = "LectureStudentRelation"
    verbose_name = "Lecture Student Relation"
    verbose_name_plural = "Lecture Student Relations"
    unique_together = ["student", "lecture_field", "day"]
    indexes = [
      models.Index(fields=["student"]),
      models.Index(fields=["lecture_field"]),
      models.Index(fields=["day"]),
      models.Index(fields=["lecture_field", "day"]),
    ]

  def __str__(self):
    return f"{self.student} - {self.lecture_field} ({self.day})"
