from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from ..models import Student, ClassStudentRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@csrf_exempt
def CheckDuplicatedStudentId(request):
  if request.method == "GET":
    student_id = request.GET.get("student_id")
    if Student.objects.filter(id=student_id).exists():
      return JsonResponse({"error": "Student ID is already registered"}, status=500)
    return JsonResponse({"status_code": 200, "data": False})
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetStudentsCount(request):
  if request.method == "GET":
    try:
      count = Student.objects.count()
      return JsonResponse({"status_code": 200, "data": {"COUNT(*)": count}})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def SearchStudent(request):
  if request.method == "GET":
    try:
      student_id = request.GET.get("student_id")
      student = Student.objects.get(id=student_id)
      data = {
        "ID": student.id,
        "FirstName": student.first_name,
        "MiddleName": student.middle_name,
        "LastName": student.last_name,
        "Gender": student.gender,
        "CreateDate": student.create_date
      }
      return JsonResponse({"status_code": 200, "data": data})
    except ObjectDoesNotExist:
      return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def InsertStudent(request):
  if request.method == "POST":
    try:
      Student.objects.create(
        id=request.POST.get("student_id"),
        first_name=request.POST.get("first_name"),
        middle_name=request.POST.get("middle_name"),
        last_name=request.POST.get("last_name"),
        gender=request.POST.get("gender"),
        face_id=request.POST.get("face_encode"),
        create_date=date.today()
      )
      return JsonResponse({"status_code": 200, "data": True})
    except IntegrityError:
      return JsonResponse({"error": "Student ID already exists"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def RemoveStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get("student_id")
      student = Student.objects.filter(id=student_id)
      if student.exists():
        student.delete()  # Also deletes ClassStudentRelation if CASCADE is set
        return JsonResponse({"status_code": 200, "data": True})
      else:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetAllStudents(request):
  if request.method == "GET":
    try:
      students = Student.objects.all()
      data = [{
        "ID": student.id,
        "FirstName": student.first_name,
        "MiddleName": student.middle_name,
        "LastName": student.last_name,
        "Gender": student.gender,
        "CreateDate": student.create_date
      } for student in students]

      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)
