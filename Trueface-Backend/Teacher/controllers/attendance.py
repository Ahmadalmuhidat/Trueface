import uuid

from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetAttendanceByClass(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    data = [current_class, date.today()]
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        TIME_FORMAT(Attendance.Time, '%%H:%%i') AS Time
      FROM
        Attendance
      LEFT JOIN
        Students
      ON
        Attendance.Student = Students.ID
      WHERE
        Attendance.Class = %s AND Attendance.Date = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def SearchAttendance(request):
  if request.method == "GET":
    attendance_id = request.GET.get("attendance_id")
    data = (attendance_id, date.today())
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        Attendance.Time
      FROM
        Attendance
      LEFT JOIN
        Students
      ON
        Attendance.Student = Students.ID
      WHERE
        Attendance.Student = %s
      AND
        Attendance.Date = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def CheckAttendance(request):
  if request.method == "GET":
    student_id = request.GET.get("student_id")
    current_class = request.GET.get("current_class")
    data = (date.today(), student_id, current_class)
    query = '''
      SELECT
        *
      FROM
        Attendance
      WHERE
        Date = %s
      AND
        Student = %s
      AND
        Class = %s
    '''
    is_present = len(Database.ExecuteGetQuery(query, data)) > 0
    return JsonResponse({"status_code": 200, "data": is_present})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

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