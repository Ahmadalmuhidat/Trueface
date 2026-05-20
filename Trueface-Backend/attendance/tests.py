import os
from datetime import date

import jwt
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APITestCase

from attendance.models import Attendance
from course.models import Course
from lecture.models import Lecture
from students.models import Student
from users.models import User


class AttendanceTests(TestCase):
  def setUp(self):
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
    self.student = Student.objects.create(id="S001", first_name="Jane", last_name="Doe", gender="Female")
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
    self.attendance = Attendance.objects.create(
      id="A101", student=self.student, lecture_field=self.lecture, time="09:15:00", date=date.today()
    )

  def test_attendance_creation(self):
    self.assertEqual(Attendance.objects.count(), 1)
    att = Attendance.objects.get(id="A101")
    self.assertEqual(att.time.strftime("%H:%M:%S"), "09:15:00")
    self.assertEqual(str(att), f"Jane Doe - CS 101 - 01 on {date.today()}")


class AttendanceAPITests(APITestCase):
  def setUp(self):
    os.environ["JWT_TOKEN_SECRET"] = "supersecret"

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
    self.student = Student.objects.create(id="S001", first_name="Jane", last_name="Doe", gender="Female")
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

    payload = {"user_id": "U001", "role": "Teacher"}
    self.teacher_token = jwt.encode(payload, "supersecret", algorithm="HS256")
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")

  def test_list_attendances(self):
    response = self.client.get("/attendances/")
    self.assertEqual(response.status_code, 200)
    # response.data contains "results" because of pagination
    self.assertEqual(len(response.data["results"]), 0)

  def test_insert_attendance(self):
    response = self.client.post(
      "/attendances/insert/", {"student_id": self.student.id, "current_lecture": self.lecture.id}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Attendance.objects.count(), 1)

  def test_delete_attendance(self):
    att = Attendance.objects.create(
      id="A102", student=self.student, lecture_field=self.lecture, time="09:15:00", date=date.today()
    )
    response = self.client.post(
      "/attendances/delete_attendance/",
      {"current_teacher": self.teacher_token, "attendance_id": att.id, "lecture_id": self.lecture.id},
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Attendance.objects.count(), 0)

  def test_clear_lecture(self):
    Attendance.objects.create(
      id="A103", student=self.student, lecture_field=self.lecture, time="09:15:00", date=date.today()
    )
    response = self.client.post(
      "/attendances/clear_lecture/", {"current_teacher": self.teacher_token, "lecture_id": self.lecture.id}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Attendance.objects.count(), 0)
