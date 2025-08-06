from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from ..models import User, Class
from ..helper import json_web_token, password, mailer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@csrf_exempt
def InsertUser(request):
  if request.method == "POST":
    try:
      generated_password = password.generate_password()

      User.objects.create(
        id=request.POST.get("user_id"),
        name=request.POST.get("name"),
        email=request.POST.get("email"),
        password=generated_password,
        role=request.POST.get("role")
      )

      mailer.SendGeneratedPasswordMail(generated_password, [request.POST.get("email")])

      return JsonResponse({"status_code": 200, "data": True})
    except IntegrityError:
      return JsonResponse({"error": "Email or ID already exists"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetUsers(request):
  if request.method == "GET":
    users = User.objects.all().values("id", "name", "email", "role")
    return JsonResponse({"status_code": 200, "data": list(users)})

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def SearchUser(request):
  if request.method == "GET":
    try:
      user_id = request.GET.get("user_id")
      user = User.objects.get(id=user_id)
      data = {
        "ID": user.id,
        "Name": user.name,
        "Email": user.email,
        "Role": user.role
      }
      return JsonResponse({"status_code": 200, "data": data})
    except ObjectDoesNotExist:
      return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def RemoveUser(request):
  if request.method == "POST":
    try:
      user_id = request.POST.get("user_id")
      user = User.objects.get(id=user_id)

      # Delete related classes (if any)
      Class.objects.filter(instructor_id=user_id).delete()
      
      user.delete()

      return JsonResponse({"status_code": 200, "data": True})
    except ObjectDoesNotExist:
      return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def checkUser(request):
  if request.method == "GET":
    email = request.GET.get("email")
    raw_password = request.GET.get("password")

    try:
      user = User.objects.get(email=email)

      if str(user.password) == str(raw_password):  # Replace with hash check in production
        payload = {
          "user_id": user.id,
          "role": user.role,
          "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = json_web_token.GenerateToken(payload)
        return JsonResponse({"status_code": 200, "data": token})
      else:
        return JsonResponse({"status_code": 401, "error": "Password incorrect"})
    except ObjectDoesNotExist:
      return JsonResponse({"status_code": 404, "error": "User not found"})
    except Exception as e:
      return J
