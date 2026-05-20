from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APITestCase

from users.models import User


class UserTests(TestCase):
  def setUp(self):
    self.user = User.objects.create(
      id="U001",
      name="John Doe",
      email="john@example.com",
      password=make_password("securepassword"),
      role="Teacher",
    )

  def test_user_creation(self):
    self.assertEqual(User.objects.count(), 1)
    user = User.objects.get(id="U001")
    self.assertEqual(user.name, "John Doe")
    self.assertEqual(user.role, "Teacher")
    self.assertEqual(str(user), "John Doe (john@example.com)")


class UserAPITests(APITestCase):
  def setUp(self):
    from authentication.utils import GenerateToken

    self.user = User.objects.create(
      id="U001",
      name="John Doe",
      email="john@example.com",
      password=make_password("securepassword"),
      role="Admin",
    )
    token = GenerateToken({"user_id": self.user.id, "role": self.user.role})
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

  def test_list_users(self):
    response = self.client.get("/users/")
    self.assertEqual(response.status_code, 200)
    # Check for paginated results
    self.assertIn("results", response.data)
    self.assertEqual(len(response.data["results"]), 1)

  def test_create_user_with_generated_password(self):
    data = {"id": "U002", "name": "Jane Smith", "email": "jane@example.com", "role": "Teacher"}
    response = self.client.post("/users/", data)
    self.assertEqual(response.status_code, 201)
    user = User.objects.get(id="U002")
    self.assertIsNotNone(user.password)
    self.assertTrue(user.password.startswith("pbkdf2_sha256$"))
