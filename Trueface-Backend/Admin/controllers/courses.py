from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models import Course, Class, Attendance, ClassStudentRelation

@csrf_exempt
def GetCourses(request):
  if request.method == "GET":
    try:
      page = int(request.GET.get('page', 1))
      page_size = int(request.GET.get('page_size', 50))
      offset = (page - 1) * page_size
      
      courses = Course.objects.all().values()[offset:offset + page_size]
      total_count = Course.objects.count()
      
      return JsonResponse({
        "status_code": 200, 
        "data": list(courses),
        "pagination": {
          "page": page,
          "page_size": page_size,
          "total_count": total_count,
          "total_pages": (total_count + page_size - 1) // page_size
        }
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def UpdateCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")
      
      try:
        course = Course.objects.get(id=course_id)
        course.title = request.POST.get("title")
        course.credit = request.POST.get("credit")
        course.maximum_units = request.POST.get("maximum_units")
        course.long_course_title = request.POST.get("long_course_title")
        course.offering_nbr = request.POST.get("offering_nbr")
        course.academic_group = request.POST.get("academic_group")
        course.subject_area = request.POST.get("subject_area")
        course.catalog_nbr = request.POST.get("catalog_nbr")
        course.campus = request.POST.get("campus")
        course.academic_organization = request.POST.get("academic_organization")
        course.component = request.POST.get("component")
        course.save()

        return JsonResponse({"status_code": 200, "data": True})
      except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found or nothing to update"}, status=404)

    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@transaction.atomic
def RemoveCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")
      
      try:
        course = Course.objects.get(id=course_id)
        classes = Class.objects.filter(course=course)

        for class_obj in classes:
          Attendance.objects.filter(class_field=class_obj).delete()

        for class_obj in classes:
          ClassStudentRelation.objects.filter(class_field=class_obj).delete()
        
        classes.delete()
        course.delete()
        
        return JsonResponse({"status_code": 200, "data": True})
      except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found or already deleted"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetLectures(request):
  if request.method == "GET":
    try:
      course_id = request.GET.get('course_id')
      classes = Class.objects.filter(course_id=course_id).select_related('instructor')
      
      data = []
      for class_obj in classes:
        data.append({
          'ID': class_obj.id,
          'SubjectArea': class_obj.subject_area,
          'CatalogNbr': class_obj.catalog_nbr,
          'AcademicCareer': class_obj.academic_career,
          'Course': class_obj.course_id,
          'OfferingNbr': class_obj.offering_nbr,
          'StartTime': class_obj.start_time,
          'EndTime': class_obj.end_time,
          'Section': class_obj.section,
          'Component': class_obj.component,
          'Campus': class_obj.campus,
          'Instructor': class_obj.instructor_id,
          'Name': class_obj.instructor.name if class_obj.instructor else None,
          'INS_ID': class_obj.instructor_id
        })
      
      return JsonResponse({
        "status_code": 200,
        "data": data
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def InsertCourse(request):
  if request.method == "POST":
    try:
      Course.objects.create(
        id=request.POST.get("course_id"),
        title=request.POST.get("title"),
        credit=request.POST.get("credit"),
        maximum_units=request.POST.get("maximum_units"),
        long_course_title=request.POST.get("long_course_title"),
        offering_nbr=request.POST.get("offering_nbr"),
        academic_group=request.POST.get("academic_group"),
        subject_area=request.POST.get("subject_area"),
        catalog_nbr=request.POST.get("catalog_nbr"),
        campus=request.POST.get("campus"),
        academic_organization=request.POST.get("academic_organization"),
        component=request.POST.get("component")
      )
      return JsonResponse({"status_code": 200,"data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)