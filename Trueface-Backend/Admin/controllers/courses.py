from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models import Course, Lecture, Attendance, LectureStudentRelation

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
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@transaction.atomic
def RemoveCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")
      course = Course.objects.get(id=course_id)
      lectures = Lecture.objects.filter(course=course)

      for lecture_obj in lectures:
        Attendance.objects.filter(lecture_field=lecture_obj).delete()

      for lecture_obj in lectures:
        LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()

      lectures.delete()
      course.delete()

      return JsonResponse({"status_code": 200,"data": True})
    except Course.DoesNotExist:
      return JsonResponse({"error": "Course not found or already deleted"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def UpdateCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")
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

      return JsonResponse({"status_code": 200,"data": True})
    except Course.DoesNotExist:
      return JsonResponse({"error": "Course not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

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
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetLectures(request):
  if request.method == "GET":
    try:
      course_id = request.GET.get('course_id')
      lectures = Lecture.objects.filter(course_id=course_id).select_related('instructor')

      data = []
      for lecture_obj in lectures:
        data.append({
          'id': lecture_obj.id,
          'subject_area': lecture_obj.subject_area,
          'catalog_nbr': lecture_obj.catalog_nbr,
          'academic_career': lecture_obj.academic_career,
          'course_id': lecture_obj.course_id,
          'offering_nbr': lecture_obj.offering_nbr,
          'start_time': lecture_obj.start_time,
          'end_time': lecture_obj.end_time,
          'section': lecture_obj.section,
          'component': lecture_obj.component,
          'campus': lecture_obj.campus,
          'instructor_id': lecture_obj.instructor_id,
          'name': lecture_obj.instructor.name if lecture_obj.instructor else None,
          'ins_id': lecture_obj.instructor_id
        })

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)
