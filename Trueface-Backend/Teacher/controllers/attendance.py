import uuid

from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def InsertAttendance(request):
  if request.method == "POST":
    student_id = request.POST.get("student_id")
    current_class = request.POST.get("current_class")
    now = datetime.now()
    AttendanceID = str(uuid.uuid4())
    date_ = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    data = (AttendanceID, student_id, current_class, time, date_)
    query = '''
      INSERT INTO
        Attendance
      VALUES
      (
        %s,
        %s,
        %s,
        %s,
        %s
      )
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })