from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..helper import json_web_token
from ..models import Class

@csrf_exempt
def get_current_teacher_classes(request):
  if request.method == "GET":
    token = request.GET.get("current_teacher")
    user_data = json_web_token.validate_token(token)

    if not user_data or "user_id" not in user_data:
      return JsonResponse({"status_code": 401, "error": "Invalid or missing token"})

    current_teacher_id = user_data["user_id"]

    classes = Class.objects.filter(instructor__id=current_teacher_id)

    data = [{
      "ID": cls.id,
      "SubjectArea": cls.subject_area,
      "StartTime": cls.start_time.strftime("%H:%M"),
      "EndTime": cls.end_time.strftime("%H:%M"),
    } for cls in classes]

    return JsonResponse({"status_code": 200, "data": data})

  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
