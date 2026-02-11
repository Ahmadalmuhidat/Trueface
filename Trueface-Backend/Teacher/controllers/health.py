from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health(request):
  if request.method == "GET":
    return JsonResponse({"status_code": 200, "data": True})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
