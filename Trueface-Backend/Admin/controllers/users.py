from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.cache import cache
from datetime import datetime, timedelta
from ..models import User, Lecture, Attendance, LectureStudentRelation
from ..helper import json_web_token, password, mailer
from ..utils.cache import cache_result, cache_invalidate

@csrf_exempt
def InsertUser(request):
  if request.method == "POST":
    generated_password = password.generate_password()

    User.objects.create(
      id=request.POST.get("user_id"),
      name=request.POST.get("name"),
      email=request.POST.get("email"),
      password=generated_password,
      role=request.POST.get("role")
    )

    # mailer.SendGeneratedPasswordMail(
    #   generated_password,
    #   [request.POST.get("email")]
    # )

    cache_invalidate("users_list")
    return JsonResponse({"status_code": 200,"data": True})
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def UpdateUser(request):
  if request.method == "POST":
    try:
      user = User.objects.get(id=request.POST.get("user_id"))
      user.name = request.POST.get("name")
      user.email = request.POST.get("email")
      user.role = request.POST.get("role")
      user.save()

      cache_invalidate("users_list")

      return JsonResponse({"status_code": 200, "data": True})
    except User.DoesNotExist:
      return JsonResponse({"error": "User not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetUsers(request):
  if request.method == "GET":
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    offset = (page - 1) * page_size
    cache_key = f"users_list_{page}_{page_size}"
    cached_result = cache.get(cache_key)

    if cached_result is None:
      users = User.objects.all().values(
        'id',
        'name',
        'email',
        'role'
      )[offset:offset + page_size]
      total_count = User.objects.count()

      result = {
        "status_code": 200,
        "data": list(users),
        "pagination": {
          "page": page,
          "page_size": page_size,
          "total_count": total_count,
          "total_pages": (total_count + page_size - 1) // page_size
        }
      }

      cache.set(cache_key, result, 300)
      return JsonResponse(result)
    else:
      return JsonResponse(cached_result)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@transaction.atomic
def RemoveUser(request):
  if request.method == "POST":
    try:
      user_id = request.POST.get("user_id")
      user = User.objects.get(id=user_id)
      lectures = Lecture.objects.filter(instructor=user)

      for lecture_obj in lectures:
        Attendance.objects.filter(lecture_field=lecture_obj).delete()

      for lecture_obj in lectures:
        LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()
      
      lectures.delete()
      user.delete()

      cache_invalidate("users_list")
      return JsonResponse({"status_code": 200,"data": True})
    except User.DoesNotExist:
      return JsonResponse({"status_code": 404,"error": "User not found or already deleted"})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def login(request):
  if request.method == "GET":
    try:
      email = request.GET.get("email")
      password = request.GET.get("password")
      user = User.objects.get(email=email)

      if str(user.password) == str(password):
        payload = {
          'user_id': user.id,
          'role': user.role,
          'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return JsonResponse({"status_code": 200,"data": json_web_token.GenerateToken(payload)})
      else:
        return JsonResponse({"status_code": 500,"error": "Password incorrect"})
    except User.DoesNotExist:
      return JsonResponse({"status_code": 500,"error": "User was not found"})
  return JsonResponse({"error": "Method not allowed"}, status=405)