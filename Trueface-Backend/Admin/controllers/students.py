from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import date
from ..models import Student, LectureStudentRelation, Attendance

@csrf_exempt
def InsertStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      first_name = request.POST.get('first_name')
      middle_name = request.POST.get('middle_name')
      last_name = request.POST.get('last_name')
      gender = request.POST.get('gender')
      student_face_encode = request.POST.get('face_encode')
      Student.objects.create(
        id=student_id,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        gender=gender,
        face_id=student_face_encode,
        create_date=date.today()
      )

      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def UpdateStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      first_name = request.POST.get('first_name')
      middle_name = request.POST.get('middle_name')
      last_name = request.POST.get('last_name')
      gender = request.POST.get('gender')

      student = Student.objects.get(id=student_id)
      student.first_name = first_name
      student.middle_name = middle_name
      student.last_name = last_name
      student.gender = gender
      student.save()

      return JsonResponse({"status_code": 200, "data": True})
    except Student.DoesNotExist:
      return JsonResponse({"error": "Student not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@transaction.atomic
def RemoveStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      student = Student.objects.get(id=student_id)
      Attendance.objects.filter(student=student).delete()
      LectureStudentRelation.objects.filter(student=student).delete()
      student.delete()

      return JsonResponse({"status_code": 200,"data": True})
    except Student.DoesNotExist:
      return JsonResponse({"error": "Student not found or already deleted"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def GetAllStudents(request):
  if request.method == "GET":
    try:
      page = int(request.GET.get('page', 1))
      page_size = int(request.GET.get('page_size', 50))
      offset = (page - 1) * page_size
      students = Student.objects.all().values(
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'gender',
        'create_date'
      )[offset:offset + page_size]
      total_count = Student.objects.count()

      return JsonResponse({
        "status_code": 200,
        "data": list(students),
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
def GetStudentLectures(request):
  if request.method == "GET":
    try:
      student_id = request.GET.get('student_id')
      relations = LectureStudentRelation.objects.filter(student_id=student_id).select_related('lecture_field')

      data = []
      for relation in relations:
        data.append({
          'id': relation.lecture_field.id,
          'subject_area': relation.lecture_field.subject_area,
          'start_time': relation.lecture_field.start_time,
          'end_time': relation.lecture_field.end_time,
          'day': relation.day
        })

      return JsonResponse({"status_code": 200,"data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def RemoveStudentFromLecture(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      lecture_id = request.POST.get('lecture_id')
      day = request.POST.get('day')
      LectureStudentRelation.objects.filter(
        student_id=student_id,
        lecture_field_id=lecture_id,
        day=day
      ).delete()

      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def AddStudentToLecture(request):
  if request.method == "POST":
    try:
      LectureStudentRelation.objects.create(
        id=request.POST.get('relation_id'),
        student_id=request.POST.get('student_id'),
        lecture_field_id=request.POST.get('lecture_id'),
        day=request.POST.get('day')
      )

      return JsonResponse({"status_code": 200,"data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({"error": "Method not allowed"}, status=405)

