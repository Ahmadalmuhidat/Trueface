# Admin models package
from .user import User
from .student import Student
from .course import Course
from .lecture import Lecture
from .lecture_student_relation import LectureStudentRelation
from .attendance import Attendance

__all__ = [
  'User',
  'Student', 
  'Course',
  'Lecture',
  'LectureStudentRelation',
  'Attendance'
]