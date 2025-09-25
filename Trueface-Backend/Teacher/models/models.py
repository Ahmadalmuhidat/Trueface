# Import models from Admin app to avoid duplication
from Admin.models import User, Student, Course, Class, ClassStudentRelation, Attendance

# Re-export for convenience
__all__ = ['User', 'Student', 'Course', 'Class', 'ClassStudentRelation', 'Attendance']
