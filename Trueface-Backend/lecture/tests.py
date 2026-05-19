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


class LectureTests(TestCase):
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

  def test_lecture_creation(self):
    self.assertEqual(Lecture.objects.count(), 1)
    lecture = Lecture.objects.get(id="L101")
    self.assertEqual(lecture.section, "01")
    self.assertEqual(str(lecture), "CS 101 - 01")


class LectureAPITests(APITestCase):
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

  def test_list_lectures(self):
    response = self.client.get("/lectures/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)

  def test_get_by_teacher(self):
    response = self.client.get("/lectures/get_by_teacher/", {"current_teacher": self.teacher_token})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data["data"]), 1)
    self.assertEqual(response.data["data"][0]["subject_area"], "CS")

  def test_delete_lecture(self):
    response = self.client.post(
      "/lectures/delete_lecture/", {"current_teacher": self.teacher_token, "lecture_id": self.lecture.id}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Lecture.objects.count(), 0)

  def test_clear_data(self):
    LectureStudentRelation.objects.create(id="R101", student=self.student, lecture_field=self.lecture, day="Monday")
    Attendance.objects.create(
      id="A101", student=self.student, lecture_field=self.lecture, time="09:15:00", date=date.today()
    )

    response = self.client.post(
      "/lectures/clear_data/", {"current_teacher": self.teacher_token, "lecture_id": self.lecture.id}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Attendance.objects.count(), 0)
    self.assertEqual(LectureStudentRelation.objects.count(), 0)
