from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetStudentsByLecture(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    today_name = date.today().strftime("%A")
    today_date = date.today().isoformat()

    data = [current_class, today_date, current_class, today_name]

    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        Students.Gender,
        Students.FaceID,
        TIME_FORMAT(Attendance.Time, '%%H:%%i') AS Time
      FROM
        Students
      JOIN
        ClassStudentRelation
      ON
        ClassStudentRelation.Student = Students.ID
      LEFT JOIN
        Attendance
      ON
        Attendance.Student = Students.ID
        AND Attendance.Class = %s
        AND Attendance.Date = %s
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