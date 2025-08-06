from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
  return JsonResponse({"status_code": 200, "data": True})
