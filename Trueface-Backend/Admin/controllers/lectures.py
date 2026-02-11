from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models import Lecture, Attendance, LectureStudentRelation

@csrf_exempt
@transaction.atomic
def RemoveLecture(request):
  if request.method == "POST":
    try:
      lecture_id = request.POST.get('lecture_id')
      lecture_obj = Lecture.objects.get(id=lecture_id)
      Attendance.objects.filter(lecture_field=lecture_obj).delete()
      LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()
      lecture_obj.delete()

      return JsonResponse({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return JsonResponse({"error": "Lecture not found or already deleted"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def UpdateLecture(request):
  if request.method == "POST":
    try:
      lecture_id = request.POST.get('lecture')

      lecture_obj = Lecture.objects.get(id=lecture_id)
      lecture_obj.subject_area = request.POST.get('subject')
      lecture_obj.catalog_nbr = request.POST.get('catalog_nbr')
      lecture_obj.academic_career = request.POST.get('academic_career')
      lecture_obj.course_id = request.POST.get('course')
      lecture_obj.offering_nbr = request.POST.get('offering_nbr')
      lecture_obj.start_time = request.POST.get('start_time')
      lecture_obj.end_time = request.POST.get('end_time')
      lecture_obj.section = request.POST.get('section')
      lecture_obj.component = request.POST.get('component')
      lecture_obj.campus = request.POST.get('campus')
      lecture_obj.instructor_id = request.POST.get('instructor')
      lecture_obj.save()

      return JsonResponse({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return JsonResponse({"error": "Lecture not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def InsertLecture(request):
  if request.method == "POST":
    try:
      Lecture.objects.create(
        id=request.POST.get('lecture_id'),
        subject_area=request.POST.get('subject'),
        catalog_nbr=request.POST.get('catalog_nbr'),
        academic_career=request.POST.get('academic_career'),
        course_id=request.POST.get('course'),
        offering_nbr=request.POST.get('offering_nbr'),
        start_time=request.POST.get('start_time'),
        end_time=request.POST.get('end_time'),
        section=request.POST.get('section'),
        component=request.POST.get('component'),
        campus=request.POST.get('campus'),
        instructor_id=request.POST.get('instructor_id')
      )

      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)