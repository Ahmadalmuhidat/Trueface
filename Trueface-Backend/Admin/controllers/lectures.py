from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

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
def UpdateLecture(request):
  if request.method == "POST":
    try:
      lecture_id = request.POST.get('class_id')
      subject = request.POST.get('subject')
      catalog_nbr = request.POST.get('catalog_nbr')
      academic_career = request.POST.get('academic_career')
      course = request.POST.get('course')
      offering_nbr = request.POST.get('offering_nbr')
      start_time = request.POST.get('start_time')
      end_time = request.POST.get('end_time')
      section = request.POST.get('section')
      component = request.POST.get('component')
      campus = request.POST.get('campus')
      instructor_id = request.POST.get('instructor_id')
      query = '''
        UPDATE Classes
        SET
          SubjectArea = %s,
          CatalogNbr = %s,
          AcademicCareer = %s,
          Course = %s,
          OfferingNbr = %s,
          StartTime = %s,
          EndTime = %s,
          Section = %s,
          Component = %s,
          Campus = %s,
          Instructor = %s
        WHERE ID = %s
      '''
      data = (
        subject,
        catalog_nbr,
        academic_career,
        course,
        offering_nbr,
        start_time,
        end_time,
        section,
        component,
        campus,
        instructor_id,
        lecture_id
      )

      updated = Database.ExecutePostQuery(query, data)
      if updated:
        return JsonResponse({"status_code": 200, "data": True})
      else:
        return JsonResponse({"error": "Lecture not found or nothing to update"}, status=404)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Method not allowed"}, status=405)

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
      data = [
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
        request.POST.get('instructor_id')
      ]
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
          Instructor
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