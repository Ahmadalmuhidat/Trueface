from django.db import models

class Course(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  title = models.CharField(max_length=255)
  credit = models.CharField(max_length=10)
  maximum_units = models.CharField(max_length=10)
  long_course_title = models.TextField(blank=True, null=True)
  offering_nbr = models.CharField(max_length=50)
  academic_group = models.CharField(max_length=100)
  subject_area = models.CharField(max_length=100)
  catalog_nbr = models.CharField(max_length=50)
  campus = models.CharField(max_length=100)
  academic_organization = models.CharField(max_length=100)
  component = models.CharField(max_length=50)
  
  class Meta:
    db_table = 'Courses'
    verbose_name = 'Course'
    verbose_name_plural = 'Courses'
    indexes = [
      models.Index(fields=['subject_area']),
      models.Index(fields=['catalog_nbr']),
    ]
  
  def __str__(self):
    return f"{self.subject_area} {self.catalog_nbr} - {self.title}"
