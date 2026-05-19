import os

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APITestCase

from authentication.utils import GenerateToken, generate_password, validate_token
from users.models import User


class AuthTests(TestCase):
  def setUp(self):
    os.environ["JWT_TOKEN_SECRET"] = "supersecret"

  def test_token_generation_and_validation(self):
    payload = {"user_id": "U101", "role": "Admin"}
    token = GenerateToken(payload)
    self.assertIsNotNone(token)

    decoded = validate_token(token)
    self.assertEqual(decoded["user_id"], "U101")
    self.assertEqual(decoded["role"], "Admin")

  def test_password_generation(self):
    pwd = generate_password(length=16, use_special_chars=True)
    self.assertEqual(len(pwd), 16)


class AuthAPITests(APITestCase):
  def setUp(self):
    os.environ["JWT_TOKEN_SECRET"] = "supersecret"
    self.user = User.objects.create(
      id="U001", name="John Doe", email="john@example.com", password=make_password("password123"), role="Teacher"
    )

  def test_login_success(self):
    response = self.client.post("/auth/login/", {"email": "john@example.com", "password": "password123"})
    self.assertEqual(response.status_code, 200)
    self.assertIn("token", response.data)

  def test_login_invalid_password(self):
    response = self.client.post("/auth/login/", {"email": "john@example.com", "password": "wrongpassword"})
    self.assertEqual(response.status_code, 401)

  def test_login_nonexistent_user(self):
    response = self.client.post("/auth/login/", {"email": "notfound@example.com", "password": "password123"})
    self.assertEqual(response.status_code, 401)

  def test_health_check(self):
    response = self.client.get("/auth/health/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["status_code"], 200)
    self.assertEqual(response.data["data"], True)

  def test_legacy_teacher_health_check(self):
    response = self.client.get("/teacher/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["status_code"], 200)
    self.assertEqual(response.data["data"], True)
