from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Course, Class
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@csrf_exempt
def GetCourses(request):
  if request.method == "GET":
    try:
      courses = Course.objects.all()
      data = [{
        "ID": course.id,
        "Title": course.title,
        "Credit": course.credit,
        "MaximumUnits": course.maximum_units,
        "LongCourseTitle": course.long_course_title,
        "OfferingNbr": course.offering_nbr,
        "AcademicGroup": course.academic_group,
        "SubjectArea": course.subject_area,
        "CatalogNbr": course.catalog_nbr,
        "Campus": course.campus,
        "AcademicOrganization": course.academic_organization,
        "Component": course.component,
      } for course in courses]

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def SearchCourses(request):
  if request.method == "GET":
    try:
      course_id = request.GET.get("course_id")
      course = Course.objects.get(id=course_id)
      data = {
        "ID": course.id,
        "Title": course.title,
        "Credit": course.credit,
        "MaximumUnits": course.maximum_units,
        "LongCourseTitle": course.long_course_title,
        "OfferingNbr": course.offering_nbr,
        "AcademicGroup": course.academic_group,
        "SubjectArea": course.subject_area,
        "CatalogNbr": course.catalog_nbr,
        "Campus": course.campus,
        "AcademicOrganization": course.academic_organization,
        "Component": course.component,
      }

      return JsonResponse({"status_code": 200, "data": data})
    except ObjectDoesNotExist:
      return JsonResponse({"error": "Course not found"}, status=404)
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
        credit=int(request.POST.get("credit")),
        maximum_units=int(request.POST.get("maximum_units")),
        long_course_title=request.POST.get("long_course_title"),
        offering_nbr=int(request.POST.get("offering_nbr")),
        academic_group=request.POST.get("academic_group"),
        subject_area=request.POST.get("subject_area"),
        catalog_nbr=int(request.POST.get("catalog_nbr")),
        campus=request.POST.get("campus"),
        academic_organization=request.POST.get("academic_organization"),
        component=request.POST.get("component"),
      )

      return JsonResponse({"status_code": 200, "data": True})
    except IntegrityError:
      return JsonResponse({"error": "Course ID already exists"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def RemoveCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")

      # Delete Classes first if needed (or let DB cascade if configured)
      Class.objects.filter(course_id=course_id).delete()
      
      deleted, _ = Course.objects.filter(id=course_id).delete()

      if deleted:
        return JsonResponse({"status_code": 200, "data": True})
      else:
        return JsonResponse({"error": "Course not found or could not be deleted"}, status=400)

    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)
