from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from ..utils.database import Database
from ..helper import json_web_token

@csrf_exempt
def get_current_teacher_classes(request):
  if request.method == "GET":
    current_teacher = json_web_token.validate_token(
      request.GET.get("current_teacher")
    ).get('user_id')

    today = date.today()
    data = [current_teacher, today]

    query = '''
      SELECT
        Classes.ID,
        Classes.SubjectArea,
        Classes.StartTime,
        Classes.EndTime
      FROM
        Classes
      JOIN
        ClassStudentRelation
      ON
        Classes.ID = ClassStudentRelation.Class
      WHERE
        Classes.Instructor = %s
      AND
        ClassStudentRelation.Day = %s
    '''
    classes = Database.ExecuteGetQuery(query, data)

    return JsonResponse({"status_code": 200, "data": classes})

  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
