from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Class, Course, User, ClassStudentRelation, Student
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@csrf_exempt
def GetClasses(request):
  if request.method == "GET":
    try:
      classes = Class.objects.select_related("course", "instructor").all()
      data = [{
        "ID": cls.id,
        "SubjectArea": cls.subject_area,
        "CatalogNbr": cls.catalog_nbr,
        "AcademicCareer": cls.academic_career,
        "OfferingNbr": cls.offering_nbr,
        "StartTime": cls.start_time.strftime("%H:%M:%S"),
        "EndTime": cls.end_time.strftime("%H:%M:%S"),
        "Section": cls.section,
        "Component": cls.component,
        "Campus": cls.campus,
        "InstructorType": cls.instructor_type,
        "Course": cls.course.title if cls.course else None,
        "Instructor": cls.instructor.name if cls.instructor else None,
      } for cls in classes]

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def SearchClass(request):
  if request.method == "GET":
    try:
      class_id = request.GET.get("class_id")
      cls = Class.objects.select_related("course").get(id=class_id)

      data = {
        "ID": cls.id,
        "SubjectArea": cls.subject_area,
        "CatalogNbr": cls.catalog_nbr,
        "AcademicCareer": cls.academic_career,
        "OfferingNbr": cls.offering_nbr,
        "StartTime": cls.start_time.strftime("%H:%M:%S"),
        "EndTime": cls.end_time.strftime("%H:%M:%S"),
        "Section": cls.section,
        "Component": cls.component,
        "Campus": cls.campus,
        "InstructorType": cls.instructor_type,
        "CourseTitle": cls.course.title if cls.course else None
      }

      return JsonResponse({"status_code": 200, "data": data})
    except ObjectDoesNotExist:
      return JsonResponse({"error": "Class not found"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def RemoveClass(request):
  if request.method == "POST":
    try:
      class_id = request.POST.get("class_id")
      Class.objects.filter(id=class_id).delete()
      ClassStudentRelation.objects.filter(class_obj_id=class_id).delete()
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def InsertClassStudentRelation(request):
  if request.method == "POST":
    try:
      relation_id = request.POST.get("relation_id")
      student_id = request.POST.get("student_id")
      class_id = request.POST.get("class_id")
      day = request.POST.get("day")

      ClassStudentRelation.objects.create(
        id=relation_id,
        student_id=student_id,
        class_obj_id=class_id,
        day=day
      )

      return JsonResponse({"status_code": 200, "data": True})
    except IntegrityError:
      return JsonResponse({"error": "Duplicate or invalid relation"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def ClearClassStudentRelation(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get("student_id")
      ClassStudentRelation.objects.filter(student_id=student_id).delete()
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def InsertClass(request):
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
        instructor_id=request.POST.get('instructor_id'),
        instructor_type=request.POST.get('instructor_type'),
      )
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def GetClassesStudentRelation(request):
  if request.method == "GET":
    try:
      student_id = request.GET.get("student_id")
      relations = ClassStudentRelation.objects.filter(student_id=student_id).select_related('class_obj')

      data = [{
        "Relation": rel.id,
        "Class": rel.class_obj.id,
        "SubjectArea": rel.class_obj.subject_area,
        "StartTime": rel.class_obj.start_time.strftime("%H:%M:%S"),
        "EndTime": rel.class_obj.end_time.strftime("%H:%M:%S"),
        "Day": rel.day
      } for rel in relations]

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def RemoveClassStudentRelation(request):
  if request.method == "POST":
    try:
      relation_id = request.POST.get("relation_id")
      ClassStudentRelation.objects.filter(id=relation_id).delete()
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def GetClassesForSelection(request):
  if request.method == "GET":
    try:
      classes = Class.objects.all()
      data = [{
        "ID": cls.id,
        "SubjectArea": cls.subject_area,
        "StartTime": cls.start_time.strftime("%H:%M:%S"),
        "EndTime": cls.end_time.strftime("%H:%M:%S")
      } for cls in classes]

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)
