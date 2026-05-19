from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from attendance.models import Attendance
from authentication.utils import validate_token
from lecture.models import Lecture, LectureStudentRelation
from lecture.serializers import LectureSerializer


class LectureViewSet(viewsets.ModelViewSet):
  queryset = Lecture.objects.select_related("course", "instructor")
  serializer_class = LectureSerializer

  @action(detail=False, methods=["get"])
  def get_by_teacher(self, request):
    try:
      current_teacher = validate_token(request.query_params.get("current_teacher")).get("user_id")
      lectures = Lecture.objects.filter(instructor_id=current_teacher).values(
        "id", "subject_area", "start_time", "end_time"
      )
      return Response({"status_code": 200, "data": list(lectures)})
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
      return Response({"status_code": 200, "data": True})
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
      return Response({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)

  # --- Legacy Desktop App Mappings ---

  def insert_legacy(self, request):
    data = request.data.copy()
    data["id"] = request.data.get("lecture_id")
    data["subject_area"] = request.data.get("subject")
    data["instructor"] = request.data.get("instructor_id")
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status_code": 200, "data": True})

  def update_legacy(self, request):
    lecture_id = request.data.get("lecture")
    lecture = Lecture.objects.get(id=lecture_id)
    data = request.data.copy()
    data["id"] = lecture_id
    data["subject_area"] = request.data.get("subject")
    data["instructor"] = request.data.get("instructor")
    serializer = self.get_serializer(lecture, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status_code": 200, "data": True})

  def destroy_legacy(self, request):
    lecture_id = request.data.get("lecture_id")
    Lecture.objects.filter(id=lecture_id).delete()
    return Response({"status_code": 200, "data": True})
