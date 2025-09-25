from django.db import models
from .user import User
from .course import Course


class Class(models.Model):
    """Class/Lecture model"""
    id = models.CharField(max_length=50, primary_key=True)
    subject_area = models.CharField(max_length=100, db_index=True)
    catalog_nbr = models.CharField(max_length=50, db_index=True)
    academic_career = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='Course', db_index=True)
    offering_nbr = models.CharField(max_length=50)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField(db_index=True)
    section = models.CharField(max_length=50)
    component = models.CharField(max_length=50)
    campus = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, db_column='Instructor', db_index=True)
    
    class Meta:
        db_table = 'Classes'
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['instructor']),
            models.Index(fields=['subject_area', 'catalog_nbr']),
            models.Index(fields=['start_time', 'end_time']),
        ]
    
    def __str__(self):
        return f"{self.subject_area} {self.catalog_nbr} - {self.section}"
