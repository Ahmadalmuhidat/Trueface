from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.models import Lecture, Attendance, LectureStudentRelation
from ..helper import json_web_token

@csrf_exempt
def GetLecturesByTeacher(request):
  if request.method == "GET":
    current_teacher = json_web_token.validate_token(request.GET.get("current_teacher")).get('user_id')

    lectures = Lecture.objects.filter(instructor_id=current_teacher).values(
      'id',
      'subject_area',
      'start_time',
      'end_time'
    )
    return JsonResponse({"status_code": 200, "data": list(lectures)})
  return JsonResponse({"status_code": 405,"error": "Method not allowed"})

@csrf_exempt
@transaction.atomic
def DeleteLecture(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(request.POST.get("current_teacher")).get('user_id')
      lecture_id = request.POST.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      Attendance.objects.filter(lecture_field=lecture_obj).delete()
      LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()
      lecture_obj.delete()

      return JsonResponse({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return JsonResponse({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"status_code": 405,"error": "Method not allowed"})

@csrf_exempt
@transaction.atomic
def ClearLectureData(request):
  if request.method == "POST":
    try:
      current_teacher = json_web_token.validate_token(request.POST.get("current_teacher")).get('user_id')
      lecture_id = request.POST.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      Attendance.objects.filter(lecture_field=lecture_obj).delete()
      LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()

      return JsonResponse({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return JsonResponse({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"status_code": 405,"error": "Method not allowed"})

