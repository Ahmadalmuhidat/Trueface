from django.db import models
from .student import Student
from .class_model import Class


class ClassStudentRelation(models.Model):
    """Many-to-many relationship between Classes and Students with additional day field"""
    id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='Student', db_index=True)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='Class', db_index=True)
    day = models.CharField(max_length=20, db_index=True)  # Day of the week
    
    class Meta:
        db_table = 'ClassStudentRelation'
        verbose_name = 'Class Student Relation'
        verbose_name_plural = 'Class Student Relations'
        unique_together = ['student', 'class_field', 'day']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['class_field']),
            models.Index(fields=['day']),
            models.Index(fields=['class_field', 'day']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.class_field} ({self.day})"
