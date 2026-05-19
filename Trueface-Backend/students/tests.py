import os
from datetime import date

import jwt
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APITestCase

from attendance.models import Attendance
from course.models import Course
from lecture.models import Lecture, LectureStudentRelation
from students.models import Student
from users.models import User


class StudentTests(TestCase):
  def setUp(self):
    self.student = Student.objects.create(id="S001", first_name="Jane", last_name="Doe", gender="Female")

  def test_student_creation(self):
    self.assertEqual(Student.objects.count(), 1)
    student = Student.objects.get(id="S001")
    self.assertEqual(student.first_name, "Jane")
    self.assertEqual(str(student), "Jane Doe")


class StudentAPITests(APITestCase):
  def setUp(self):
    # Set environment secret for JWT testing
    os.environ["JWT_TOKEN_SECRET"] = "supersecret"

    self.student = Student.objects.create(id="S001", first_name="Jane", last_name="Doe", gender="Female")
    self.course = Course.objects.create(
      id="CS101",
      title="CS 101",
      credit="4",
      maximum_units="4",
      offering_nbr="1",
      academic_group="ENG",
      subject_area="CS",
      catalog_nbr="101",
      campus="Main",
      academic_organization="CS Dept",
      component="LEC",
    )
    self.instructor = User.objects.create(
      id="U001",
      name="Instructor Bob",
      email="bob@example.com",
      password=make_password("password123"),
      role="Teacher",
    )
    self.lecture = Lecture.objects.create(
      id="L101",
      subject_area="CS",
      catalog_nbr="101",
      academic_career="UGRD",
      course=self.course,
      offering_nbr="1",
      start_time="09:00:00",
      end_time="10:30:00",
      section="01",
      component="LEC",
      campus="Main",
      instructor=self.instructor,
    )

    # Generate a teacher token
    payload = {"user_id": "U001", "role": "Teacher"}
    self.teacher_token = jwt.encode(payload, "supersecret", algorithm="HS256")

  def test_list_students(self):
    response = self.client.get("/students/")
    self.assertEqual(response.status_code, 200)
    self.assertIn("data", response.data)

  def test_student_lectures(self):
    # Create relation
    LectureStudentRelation.objects.create(id="R101", student=self.student, lecture_field=self.lecture, day="Monday")
    response = self.client.get(f"/students/{self.student.id}/lectures/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["day"], "Monday")

  def test_add_remove_lecture(self):
    # Add
    response = self.client.post(
      f"/students/{self.student.id}/add_lecture/",
      {"relation_id": "R102", "lecture_id": self.lecture.id, "day": "Wednesday"},
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(LectureStudentRelation.objects.filter(day="Wednesday").count(), 1)

    # Delete
    response = self.client.delete(
      f"/students/{self.student.id}/remove_lecture/",
      {"lecture_id": self.lecture.id, "day": "Wednesday"},
      format="json",
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(LectureStudentRelation.objects.filter(day="Wednesday").count(), 0)

  def test_get_by_lecture(self):
    today_name = date.today().strftime("%A")
    LectureStudentRelation.objects.create(id="R103", student=self.student, lecture_field=self.lecture, day=today_name)
    response = self.client.get("/students/get_by_lecture/", {"current_lecture": self.lecture.id})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data["data"]), 1)
    self.assertEqual(response.data["data"][0]["first_name"], "Jane")

  def test_remove_from_lecture(self):
    today_name = date.today().strftime("%A")
    LectureStudentRelation.objects.create(id="R104", student=self.student, lecture_field=self.lecture, day=today_name)
    response = self.client.post(
      "/students/remove_from_lecture/",
      {
        "current_teacher": self.teacher_token,
        "student_id": self.student.id,
        "lecture_id": self.lecture.id,
        "day": today_name,
      },
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(LectureStudentRelation.objects.filter(student=self.student).count(), 0)

  def test_clear_attendance(self):
    Attendance.objects.create(
      id="A101", student=self.student, lecture_field=self.lecture, time="09:15:00", date=date.today()
    )
    response = self.client.post(
      "/students/clear_attendance/",
      {"current_teacher": self.teacher_token, "student_id": self.student.id, "lecture_id": self.lecture.id},
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Attendance.objects.filter(student=self.student).count(), 0)
