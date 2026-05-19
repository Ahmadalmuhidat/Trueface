from django.test import TestCase
from rest_framework.test import APITestCase

from course.models import Course


class CourseTests(TestCase):
  def setUp(self):
    self.course = Course.objects.create(
      id="C101",
      title="Introduction to Computer Science",
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

  def test_course_creation(self):
    self.assertEqual(Course.objects.count(), 1)
    course = Course.objects.get(id="C101")
    self.assertEqual(course.title, "Introduction to Computer Science")
    self.assertEqual(str(course), "CS 101 - Introduction to Computer Science")


class CourseAPITests(APITestCase):
  def setUp(self):
    self.course = Course.objects.create(
      id="CS101",
      title="Intro to CS",
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

  def test_list_courses(self):
    response = self.client.get("/courses/")
    self.assertEqual(response.status_code, 200)
    self.assertTrue(any(c["id"] == "CS101" for c in response.data["data"]))

  def test_legacy_list_courses(self):
    response = self.client.get("/admin/courses/")
    self.assertEqual(response.status_code, 200)
    self.assertIn("data", response.data)
    self.assertTrue(any(c["id"] == "CS101" for c in response.data["data"]))

  def test_create_course(self):
    data = {
      "id": "CS102",
      "title": "Data Structures",
      "credit": "4",
      "maximum_units": "4",
      "offering_nbr": "1",
      "academic_group": "ENG",
      "subject_area": "CS",
      "catalog_nbr": "102",
      "campus": "Main",
      "academic_organization": "CS Dept",
      "component": "LEC",
    }
    response = self.client.post("/courses/", data)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Course.objects.count(), 2)
