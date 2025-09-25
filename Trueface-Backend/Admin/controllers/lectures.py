from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models import Class, Attendance, ClassStudentRelation

@csrf_exempt
@transaction.atomic
def RemoveLecture(request):
  if request.method == "POST":
    try:
      class_id = request.POST.get('class_id')

      try:
        class_obj = Class.objects.get(id=class_id)
        
        Attendance.objects.filter(class_field=class_obj).delete()
        ClassStudentRelation.objects.filter(class_field=class_obj).delete()

        class_obj.delete()
        
        return JsonResponse({
          "status_code": 200,
          "data": True
        })
      except Class.DoesNotExist:
        return JsonResponse({"error": "Lecture not found or already deleted"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def UpdateLecture(request):
  if request.method == "POST":
    try:
      lecture_id = request.POST.get('lecture')
      
      try:
        class_obj = Class.objects.get(id=lecture_id)
        class_obj.subject_area = request.POST.get('subject')
        class_obj.catalog_nbr = request.POST.get('catalog_nbr')
        class_obj.academic_career = request.POST.get('academic_career')
        class_obj.course_id = request.POST.get('course')
        class_obj.offering_nbr = request.POST.get('offering_nbr')
        class_obj.start_time = request.POST.get('start_time')
        class_obj.end_time = request.POST.get('end_time')
        class_obj.section = request.POST.get('section')
        class_obj.component = request.POST.get('component')
        class_obj.campus = request.POST.get('campus')
        class_obj.instructor_id = request.POST.get('instructor')
        class_obj.save()
        
        return JsonResponse({"status_code": 200, "data": True})
      except Class.DoesNotExist:
        return JsonResponse({"error": "Lecture not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def InsertLecture(request):
  if request.method == "POST":
    try:
      Class.objects.create(
        id=request.POST.get('class_id'),
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
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)
