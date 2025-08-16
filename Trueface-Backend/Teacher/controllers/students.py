import base64

from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetStudentsByClass(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[date.today().weekday()]
    data = (current_class, today)
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        Students.Gender,
        Students.FaceID
      FROM
        Students
      JOIN
        ClassStudentRelation
      ON
        ClassStudentRelation.Student = Students.ID
      WHERE
        ClassStudentRelation.Class = %s
      AND
        ClassStudentRelation.Day = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })