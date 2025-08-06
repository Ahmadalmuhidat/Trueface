import base64
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Student, ClassStudentRelation


@csrf_exempt
def get_class_students(request):
  if request.method == "GET":
    class_id = request.GET.get("current_class")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[date.today().weekday()]

    students = Student.objects.filter(
      classstudentrelation__class_obj__id=class_id,
      classstudentrelation__day=today
    ).distinct()

    data = [{
      "ID": student.id,
      "FirstName": student.first_name,
      "MiddleName": student.middle_name,
      "LastName": student.last_name,
      "Gender": student.gender
    } for student in students]

    return JsonResponse({"status_code": 200, "data": data})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})


@csrf_exempt
def get_students_with_face_encode(request):
  if request.method == "GET":
    class_id = request.GET.get("current_class")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[date.today().weekday()]

    students = Student.objects.filter(
      classstudentrelation__class_obj__id=class_id,
      classstudentrelation__day=today
    ).distinct()

    data = []
    for student in students:
      face_encoded = ""
      if isinstance(student.face_id, bytes):
        face_encoded = base64.b64encode(student.face_id).decode('utf-8')
      else:
        face_encoded = student.face_id  # in case it's stored as string (text field)

      data.append({
        "ID": student.id,
        "FirstName": student.first_name,
        "MiddleName": student.middle_name,
        "LastName": student.last_name,
        "Gender": student.gender,
        "FaceID": face_encoded,
        "CreateDate": student.create_date.strftime("%Y-%m-%d")
      })

    return JsonResponse({"status_code": 200, "data": data})
  return JsonResponse({"status_code": 405, "error": "Method not allowed"})
