from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from ..utils.database import Database
from ..helper import json_web_token, password, mailer

@csrf_exempt
def InsertUser(request):
  if request.method == "POST":
    generated_password = password.generate_password()
    data = [
      request.POST.get("user_id"),
      request.POST.get("name"),
      request.POST.get("email"),
      generated_password,
      request.POST.get("role")
    ]
    query = '''
      INSERT INTO
        Users
      VALUES
      (
        %s,
        %s,
        %s,
        %s,
        %s
      )
    '''

    mailer.SendGeneratedPasswordMail(generated_password,  [request.POST.get("email")])

    return JsonResponse({
      "status_code": 200,
      "data": Database.ExecutePostQuery(query, data)
    })
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetUsers(request):
  if request.method == "GET":
    query = '''
      SELECT
        ID,
        Name,
        Email,
        Role
      FROM
        Users
    '''
    return JsonResponse({
      "status_code": 200,
      "data": Database.ExecuteGetQuery(query)
    })
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveUser(request):
  if request.method == "POST":
    user_id = request.POST.get("user_id")
    data = [user_id]

    delete_user_query = 'DELETE FROM Users WHERE ID = %s'
    remove = Database.ExecutePostQuery(delete_user_query, data)

    if remove:
      delete_classes_query = '''
        DELETE FROM
          Classes
        WHERE
          Instructor = %s
      '''
      Database.ExecutePostQuery(delete_classes_query, data)
      return JsonResponse({
        "status_code": 200,
        "data": True
      })
    else:
      return JsonResponse({
        "status_code": 500,
        "error": "Something went wrong while deleting the student"
      })
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def login(request):
  if request.method == "GET":
    email = request.GET.get("email")
    password = request.GET.get("password")
    data = (email,)
    query = '''
      SELECT
        ID,
        Password,
        Role
      FROM
        Users
      WHERE
        Email = %s
    '''
    user = Database.ExecuteGetQuery(query, data)

    if len(user) == 1:
      if str(user[0]['Password']) == str(password):
        payload = {
          'user_id': user[0]['ID'],
          'role': user[0]['Role'],
          'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return JsonResponse({
          "status_code": 200,
          "data": json_web_token.GenerateToken(payload)
        })
      else:
        return JsonResponse({
          "status_code": 500,
          "error": "Password incorrect"
        })
    else:
      return JsonResponse({
        "status_code": 500,
        "error": "User was not found"
      })
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)