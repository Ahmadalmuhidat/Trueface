from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetCourses(request):
  if request.method == "GET":
    try:
      query = '''
        SELECT
          *
        FROM
          Courses
      '''
      data = Database.ExecuteGetQuery(query)
      return JsonResponse({"status_code": 200, "data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveCourse(request):
  if request.method == "POST":
    try:
      course_id = request.POST.get("course_id")
      query = "DELETE FROM Courses WHERE ID = %s"
      removed = Database.ExecutePostQuery(query, [course_id])

      if removed:
        query = "DELETE FROM Classes WHERE Course = %s"
        Database.ExecutePostQuery(query, [course_id])
        return JsonResponse({"status_code": 200,"data": True})
      else:
        return JsonResponse({"error": "Something went wrong while deleting the course"}, status=500)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def InsertCourse(request):
  if request.method == "POST":
    try:
      data = (
        request.POST.get("course_id"),
        request.POST.get("title"),
        request.POST.get("credit"),
        request.POST.get("maximum_units"),
        request.POST.get("long_course_title"),
        request.POST.get("offering_nbr"),
        request.POST.get("academic_group"),
        request.POST.get("subject_area"),
        request.POST.get("catalog_nbr"),
        request.POST.get("campus"),
        request.POST.get("academic_organization"),
        request.POST.get("component"),
      )

      query = '''
        INSERT INTO
          Courses
        VALUES (
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
      return JsonResponse({"status_code": 200,"data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)