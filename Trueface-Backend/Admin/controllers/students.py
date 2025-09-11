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
def UpdateStudent(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      first_name = request.POST.get('first_name')
      middle_name = request.POST.get('middle_name')
      last_name = request.POST.get('last_name')
      gender = request.POST.get('gender')

      query = '''
        UPDATE Students
        SET
          FirstName = %s,
          MiddleName = %s,
          LastName = %s,
          Gender = %s
        WHERE ID = %s
      '''
      data = (
        first_name,
        middle_name,
        last_name,
        gender,
        student_id
      )

      updated = Database.ExecutePostQuery(query, data)

      if updated:
        return JsonResponse({"status_code": 200, "data": True})
      else:
        return JsonResponse({"error": "Student not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

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

@csrf_exempt
def ClearLectures(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      query = '''
        DELETE FROM
          ClassStudentRelation
        WHERE
          Student = %s
      '''
      Database.ExecutePostQuery(query, [student_id])
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetStudentLectures(request):
  if request.method == "GET":
    try:
      student_id = request.GET.get('student_id')
      data = [student_id]
      query = '''
        SELECT
          Classes.ID,
          Classes.SubjectArea,
          Classes.StartTime,
          Classes.EndTime,
          ClassStudentRelation.Day
        FROM
          Classes
        JOIN
          ClassStudentRelation
        ON
          Classes.ID = ClassStudentRelation.Class
        WHERE
          ClassStudentRelation.Student = %s
      '''
      data = Database.ExecuteGetQuery(query, data)
      return JsonResponse({"status_code": 200,"data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveStudentFromLecture(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      lecture_id = request.POST.get('lecture_id')
      day = request.POST.get('day')

      data = [student_id, lecture_id, day]
      query = '''
        DELETE FROM
          ClassStudentRelation
        WHERE
          Student = %s
        AND
          Class = %s
        AND
          Day = %s
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def AddStudentToLecture(request):
  if request.method == "POST":
    try:
      data = (
        request.POST.get('relation_id'),
        request.POST.get('student_id'),
        request.POST.get('class_id'),
        request.POST.get('day')
      )
      query = '''
        INSERT INTO
          ClassStudentRelation
          (
            ID,
            Student,
            Class,
            Day
          )
        VALUES
        (
          %s, 
          %s,
          %s,
          %s
        )
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({"status_code": 200,"data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)