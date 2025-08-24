from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from ..utils.database import Database

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

      data = [
        student_id,
        first_name,
        middle_name,
        last_name,
        gender,
        student_face_encode,
        date.today()
      ]
      query = '''
        INSERT INTO
          Students
        VALUES
        (
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s
        )
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({
        "status_code": 200,
        "data": True
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      data = [student_id]

      # remove the student
      query = '''
        DELETE FROM
          Students
        WHERE
          ID = %s
      '''
      remove_the_student = Database.ExecutePostQuery(query, data)

      if remove_the_student:
        # remove the student from the classes
        query = '''
          DELETE FROM
            ClassStudentRelation
          WHERE
            Student = %s
        '''
        Database.ExecutePostQuery(query, data)
        return JsonResponse({
          "status_code": 200,
          "data": True
        })
      else:
        return JsonResponse({"error": "error while removing the student"}, status=500)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetAllStudents(request):
  if request.method == "GET":
    try:
      query = '''
        SELECT
          ID,
          FirstName,
          MiddleName,
          LastName,
          Gender,
          CreateDate
        FROM
          Students
      '''
      result = Database.ExecuteGetQuery(query)
      return JsonResponse({
        "status_code": 200,
        "data": result
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)
