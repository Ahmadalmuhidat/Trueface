from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.models import Lecture, Attendance, LectureStudentRelation
from ..helper import json_web_token

@csrf_exempt
def GetStudentsByLecture(request):
  if request.method == "GET":
    current_lecture = request.GET.get("current_lecture")
    today_name = date.today().strftime("%A")
    today_date = date.today().isoformat()

    relations = LectureStudentRelation.objects.filter(
      lecture_field_id=current_lecture,
      day=today_name
    ).select_related('student').prefetch_related(
      'student__attendance_set'
    )
    
    attendance_records = {
      att.student_id: att.time.strftime('%H:%M') 
      for att in Attendance.objects.filter(
        lecture_field_id=current_lecture,
        date=today_date
      ).select_related('student')
    }
    
    data = []
    for relation in relations:
      student = relation.student
      data.append({
        'id': student.id,
        'first_name': student.first_name,
        'middle_name': student.middle_name,
        'last_name': student.last_name,
        'gender': student.gender,
        'face_id': student.face_id,
        'time': attendance_records.get(student.id)
      })
    
    return JsonResponse({"status_code": 200, "data": data})

  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
@transaction.atomic
def RemoveStudentFromLecture(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      student_id = request.POST.get("student_id")
      lecture_id = request.POST.get("lecture_id")
      day = request.POST.get("day")
      
      try:
        lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
        
        Attendance.objects.filter(
          student_id=student_id,
          lecture_field=lecture_obj
        ).delete()
        
        relation = LectureStudentRelation.objects.filter(
          student_id=student_id,
          lecture_field=lecture_obj,
          day=day
        ).first()
        
        if relation:
          relation.delete()
          return JsonResponse({"status_code": 200, "data": True})
        else:
          return JsonResponse({"error": "Student not found in this lecture"}, status=404)
      except Lecture.DoesNotExist:
        return JsonResponse({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
@transaction.atomic
def ClearStudentAttendance(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      student_id = request.POST.get("student_id")
      lecture_id = request.POST.get("lecture_id")
      
      try:
        lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
        attendance_count = Attendance.objects.filter(
          student_id=student_id,
          lecture_field=lecture_obj
        ).count()
        
        if attendance_count > 0:
          Attendance.objects.filter(
            student_id=student_id,
            lecture_field=lecture_obj
          ).delete()
          return JsonResponse({"status_code": 200, "data": True})
        else:
          return JsonResponse({"error": "No attendance records found"}, status=404)
      except Lecture.DoesNotExist:
        return JsonResponse({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })