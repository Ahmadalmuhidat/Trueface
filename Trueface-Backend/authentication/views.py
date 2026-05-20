from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import GenerateToken
from users.models import User


class LoginView(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
      user = User.objects.get(email=email)

      if not check_password(password, user.password):
        return Response({"error": "Invalid credentials"}, status=401)

      payload = {"user_id": user.id, "role": user.role, "exp": datetime.utcnow() + timedelta(hours=24)}

      token = GenerateToken(payload)
      return Response({"token": token})

    except User.DoesNotExist:
      return Response({"error": "Invalid credentials"}, status=401)

  def get(self, request):
    email = request.query_params.get("email")
    password = request.query_params.get("password")

    try:
      user = User.objects.get(email=email)

      if not check_password(password, user.password):
        return Response({"status_code": 401, "error": "Invalid credentials"}, status=401)

      payload = {"user_id": user.id, "role": user.role, "exp": datetime.utcnow() + timedelta(hours=24)}

      token = GenerateToken(payload)
      return Response({"status_code": 200, "data": {"token": token}})

    except User.DoesNotExist:
      return Response({"status_code": 401, "error": "Invalid credentials"}, status=401)


class HealthView(APIView):
  permission_classes = [AllowAny]
  def get(self, request, *args, **kwargs):
    return Response({"status_code": 200, "data": True})
