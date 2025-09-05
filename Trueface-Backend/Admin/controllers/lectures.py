from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetLectures(request):
  if request.method == "GET":
    try:
      course_id = request.GET.get('course_id')
      data = [course_id]
      query = '''
        SELECT
          Classes.*, Users.Name
        FROM
          Classes
        LEFT JOIN
          Users
        ON
          Classes.Instructor = Users.ID
        WHERE
          Classes.Course = %s
      '''
      data = Database.ExecuteGetQuery(query, data)
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
def RemoveLecture(request):
  if request.method == "POST":
    try:
      
      class_id = request.POST.get('class_id')
      query = '''
        DELETE FROM
          Classes
        WHERE
          ID = %s
      '''
      if Database.ExecutePostQuery(query, [class_id]):
        query = '''
          DELETE FROM
            ClassStudentRelation
          WHERE
            Class = %s
        '''
        Database.ExecutePostQuery(query, [class_id])
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

@csrf_exempt
def ClearLecture(request):
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
def InsertLecture(request):
  if request.method == "POST":
    try:
      data = (
        request.POST.get('class_id'),
        request.POST.get('subject'),
        request.POST.get('catalog_nbr'),
        request.POST.get('academic_career'),
        request.POST.get('course'),
        request.POST.get('offering_nbr'),
        request.POST.get('start_time'),
        request.POST.get('end_time'),
        request.POST.get('section'),
        request.POST.get('component'),
        request.POST.get('campus'),
        request.POST.get('instructor_id'),
        request.POST.get('instructor_type'),
      )
      query = '''
        INSERT INTO
        Classes
        (
          ID,
          SubjectArea,
          CatalogNbr,
          AcademicCareer,
          Course,
          OfferingNbr,
          StartTime,
          EndTime,
          Section,
          Component,
          Campus,
          Instructor,
          InstructorType
        )
        VALUES
        (
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
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
def GetClassesForSelection(request):
  if request.method == "GET":
    try:
      query = '''
        SELECT
          ID,
          SubjectArea,
          StartTime,
          EndTime
        FROM
          Classes
      '''
      data = Database.ExecuteGetQuery(query)
      return JsonResponse({"status_code": 200,"data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)