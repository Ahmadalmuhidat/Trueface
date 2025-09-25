from django.db import models
from .student import Student
from .class_model import Class


class Attendance(models.Model):
    """Attendance model"""
    id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='Student', db_index=True)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='Class', db_index=True)
    time = models.TimeField(db_index=True)
    date = models.DateField(db_index=True)
    
    class Meta:
        db_table = 'Attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['student', 'class_field', 'date']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['class_field']),
            models.Index(fields=['date']),
            models.Index(fields=['class_field', 'date']),
            models.Index(fields=['student', 'class_field']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.class_field} on {self.date}"
