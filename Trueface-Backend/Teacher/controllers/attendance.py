import uuid
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q, Value, Case, When
from django.db.models.functions import Cast
from django.db.models import CharField
from .models import Attendance, Student, Class


@csrf_exempt
def get_current_class_attendance(request):
  if request.method == "GET":
    current_class_id = request.GET.get("current_class")
    today = date.today()

    attendance = Attendance.objects.filter(
      class_obj__id=current_class_id,
      date__date=today
    ).select_related('student')

    data = [{
      "ID": att.student.id,
      "FirstName": att.student.first_name,
      "MiddleName": att.student.middle_name,
      "LastName": att.student.last_name,
      "Time": att.time.strftime("%H:%M") if att.time else None
    } for att in attendance]

    return JsonResponse({"status_code": 200, "data": data})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})


@csrf_exempt
def search_attendance(request):
  if request.method == "GET":
    student_id = request.GET.get("attendance_id")
    today = date.today()

    attendance = Attendance.objects.filter(
      student__id=student_id,
      date__date=today
    ).select_related('student')

    data = [{
      "ID": att.student.id,
      "FirstName": att.student.first_name,
      "MiddleName": att.student.middle_name,
      "LastName": att.student.last_name,
      "Time": att.time.strftime("%H:%M:%S") if att.time else None
    } for att in attendance]

    return JsonResponse({"status_code": 200, "data": data})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})


@csrf_exempt
def check_attendance(request):
  if request.method == "GET":
    student_id = request.GET.get("student_id")
    class_id = request.GET.get("current_class")
    today = date.today()

    is_present = Attendance.objects.filter(
      student__id=student_id,
      class_obj__id=class_id,
      date__date=today
    ).exists()

    return JsonResponse({"status_code": 200, "data": is_present})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})


@csrf_exempt
def insert_attendance(request):
  if request.method == "POST":
    student_id = request.POST.get("student_id")
    class_id = request.POST.get("current_class")

    now = datetime.now()
    attendance = Attendance.objects.create(
      id=str(uuid.uuid4()),
      student_id=student_id,
      class_obj_id=class_id,
      time=now.time(),
      date=now
    )

    return JsonResponse({"status_code": 200, "data": {
      "AttendanceID": attendance.id,
      "StudentID": student_id,
      "ClassID": class_id,
      "Time": now.strftime("%H:%M:%S"),
      "Date": now.strftime("%Y-%m-%d")
    }})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})


@csrf_exempt
def get_class_attendance_report(request):
  if request.method == "GET":
    start_time_str = request.GET.get("start_time")
    allowed_minutes = int(request.GET.get("allowed_minutes")) * 60
    class_id = request.GET.get("current_class")
    today = date.today()

    start_time = datetime.strptime(start_time_str, "%H:%M").time()

    students = Student.objects.all().annotate(
      attendance_time=F('attendance__time'),
      attendance_date=F('attendance__date'),
      attendance_class=F('attendance__class_obj')
    ).filter(
      Q(attendance_date__date=today) | Q(attendance_date__isnull=True),
      Q(attendance_class__id=class_id) | Q(attendance_class__isnull=True)
    ).distinct()

    data = []
    for s in students:
      if s.attendance_time is None:
        time_val = "absent"
        lateness = False
      else:
        time_val = s.attendance_time.strftime("%H:%M")
        diff_seconds = (
          datetime.combine(today, s.attendance_time) -
          datetime.combine(today, start_time)
        ).total_seconds()
        lateness = "late" if diff_seconds > allowed_minutes else "not late"

      data.append({
        "ID": s.id,
        "FirstName": s.first_name,
        "MiddleName": s.middle_name,
        "LastName": s.last_name,
        "Time": time_val,
        "Lateness": lateness
      })

    return JsonResponse({"status_code": 200, "data": data})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})
