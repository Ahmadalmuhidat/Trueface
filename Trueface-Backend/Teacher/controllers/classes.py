from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from ..utils.database import Database
from ..helper import json_web_token

@csrf_exempt
def GetClassesByTeacher(request):
  if request.method == "GET":
    current_teacher = json_web_token.validate_token(
      request.GET.get("current_teacher")
    ).get('user_id')

    data = [current_teacher]
    query = '''
      SELECT
        ID,
        SubjectArea,
        StartTime,
        EndTime
      FROM
        Classes
      WHERE
        Instructor = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})

  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
