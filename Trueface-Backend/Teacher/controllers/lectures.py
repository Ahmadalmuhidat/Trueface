from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.models import Class, Attendance, ClassStudentRelation
from ..helper import json_web_token

@csrf_exempt
def GetLecturesByTeacher(request):
  if request.method == "GET":
    current_teacher = json_web_token.validate_token(
      request.GET.get("current_teacher")
    ).get('user_id')

    classes = Class.objects.filter(instructor_id=current_teacher).values(
      'id', 'subject_area', 'start_time', 'end_time'
    )
    return JsonResponse({"status_code": 200, "data": list(classes)})

  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
@transaction.atomic
def DeleteLecture(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      class_id = request.POST.get("class_id")
      
      try:
        class_obj = Class.objects.get(id=class_id, instructor_id=current_teacher)
        
        Attendance.objects.filter(class_field=class_obj).delete()
        ClassStudentRelation.objects.filter(class_field=class_obj).delete()
        
        class_obj.delete()
        
        return JsonResponse({"status_code": 200, "data": True})
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
def ClearLectureData(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(
        request.POST.get("current_teacher")
      ).get('user_id')
      
      class_id = request.POST.get("class_id")
      
      try:
        class_obj = Class.objects.get(id=class_id, instructor_id=current_teacher)
        
        Attendance.objects.filter(class_field=class_obj).delete()
        ClassStudentRelation.objects.filter(class_field=class_obj).delete()
        
        return JsonResponse({"status_code": 200, "data": True})
      except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
