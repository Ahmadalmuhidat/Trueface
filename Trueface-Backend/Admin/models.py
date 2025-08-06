from django.db import models

class Course(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  title = models.CharField(max_length=200)
  credit = models.IntegerField()
  maximum_units = models.IntegerField()
  long_course_title = models.CharField(max_length=200)
  offering_nbr = models.IntegerField()
  academic_group = models.CharField(max_length=200)
  subject_area = models.CharField(max_length=200)
  catalog_nbr = models.IntegerField()
  campus = models.CharField(max_length=200)
  academic_organization = models.CharField(max_length=200)
  component = models.CharField(max_length=200)

  def __str__(self):
    return self.title

class Instructor(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  first_name = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200, blank=True, null=True)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(max_length=200)
  password = models.CharField(max_length=200)
  create_date = models.DateField()

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class Class(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  subject_area = models.CharField(max_length=200)
  catalog_nbr = models.IntegerField()
  academic_career = models.CharField(max_length=200)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  offering_nbr = models.IntegerField()
  start_time = models.TimeField()
  end_time = models.TimeField()
  section = models.CharField(max_length=200)
  component = models.CharField(max_length=200)
  campus = models.CharField(max_length=200)
  instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
  instructor_type = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.subject_area} {self.catalog_nbr} - {self.section}"

class ClassStudentRelation(models.Model):
  student = models.ForeignKey('Student', on_delete=models.CASCADE)
  class_obj = models.ForeignKey('Class', on_delete=models.CASCADE)
  day = models.CharField(max_length=20)

  class Meta:
    unique_together = ('student', 'class_obj', 'day')

class Student(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  first_name = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200, blank=True, null=True)
  last_name = models.CharField(max_length=200)
  gender = models.CharField(max_length=200)
  face_id = models.TextField()
  create_date = models.DateField()

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class')  # 'class' is a reserved keyword
  time = models.TimeField()
  date = models.DateTimeField()

  def __str__(self):
    return f"Attendance: {self.student} - {self.class_obj} on {self.date}"

class User(models.Model):
  id = models.CharField(max_length=200, primary_key=True)
  name = models.CharField(max_length=200)
  email = models.EmailField(max_length=200)
  password = models.CharField(max_length=200)
  role = models.CharField(max_length=200)

  def __str__(self):
    return self.name