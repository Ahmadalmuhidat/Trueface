import uuid

from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.models import Attendance, Class
from ..helper import json_web_token

@csrf_exempt
def InsertAttendance(request):
  if request.method == "POST":
    student_id = request.POST.get("student_id")
    current_class = request.POST.get("current_class")
    now = datetime.now()
    attendance_id = str(uuid.uuid4())
    date_ = now.date()
    time = now.time()

    Attendance.objects.create(
      id=attendance_id,
      student_id=student_id,
      class_field_id=current_class,
      time=time,
      date=date_
    )
    return JsonResponse({"status_code": 200, "data": True})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
@transaction.atomic
def DeleteAttendance(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      attendance_id = request.POST.get("attendance_id")
      class_id = request.POST.get("class_id")
      
      try:
        class_obj = Class.objects.get(id=class_id, instructor_id=current_teacher)
        
        attendance = Attendance.objects.filter(
          id=attendance_id,
          class_field=class_obj
        ).first()
        
        if attendance:
          attendance.delete()
          return JsonResponse({"status_code": 200, "data": True})
        else:
          return JsonResponse({"error": "Attendance record not found"}, status=404)
      except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
@transaction.atomic
def ClearClassAttendance(request):
  if request.method == "POST":
    try:
      # Verify teacher owns this class
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      class_id = request.POST.get("class_id")
      
      try:
        # Verify teacher owns this class
        class_obj = Class.objects.get(id=class_id, instructor_id=current_teacher)
        
        # Clear all attendance for this class
        Attendance.objects.filter(class_field=class_obj).delete()
        
        return JsonResponse({"status_code": 200, "data": True})
      except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })