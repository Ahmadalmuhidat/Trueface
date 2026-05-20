from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance
from authentication.utils import validate_token
from lecture.models import Lecture, LectureStudentRelation
from lecture.pagination import CustomPagination
from lecture.serializers import LectureSerializer


class LectureViewSet(viewsets.ModelViewSet):
  queryset = Lecture.objects.select_related("course", "instructor")
  serializer_class = LectureSerializer
  pagination_class = CustomPagination
  permission_classes = [IsAuthenticated]

  @action(detail=False, methods=["get"])
  def get_by_teacher(self, request):
    try:
      current_teacher = validate_token(request.query_params.get("current_teacher")).get("user_id")
      lectures = Lecture.objects.filter(instructor_id=current_teacher).values(
        "id", "subject_area", "start_time", "end_time"
      )
      return Response(list(lectures))
    except Exception as e:
      return Response({"error": str(e)}, status=500)

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def delete_lecture(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      lecture_id = request.data.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      lecture_obj.delete()
      return Response({"success": True})
    except Lecture.DoesNotExist:
      return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def clear_data(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      lecture_id = request.data.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      Attendance.objects.filter(lecture_field=lecture_obj).delete()
      LectureStudentRelation.objects.filter(lecture_field=lecture_obj).delete()
      return Response({"success": True})
    except Lecture.DoesNotExist:
      return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)
