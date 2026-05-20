import uuid
from datetime import datetime

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from attendance.models import Attendance
from attendance.pagination import CustomPagination
from attendance.serializers import AttendanceSerializer
from authentication.utils import validate_token
from lecture.models import Lecture


class AttendanceViewSet(viewsets.ModelViewSet):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer
  pagination_class = CustomPagination

  @action(detail=False, methods=["post"])
  def insert(self, request):
    student_id = request.data.get("student_id")
    current_lecture = request.data.get("current_lecture")
    now = datetime.now()
    Attendance.objects.create(
      id=str(uuid.uuid4()),
      student_id=student_id,
      lecture_field_id=current_lecture,
      time=now.time(),
      date=now.date(),
    )
    return Response({"status_code": 200, "data": True})

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def delete_attendance(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      attendance_id = request.data.get("attendance_id")
      lecture_id = request.data.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      attendance = Attendance.objects.filter(id=attendance_id, lecture_field=lecture_obj).first()

      if attendance:
        attendance.delete()
        return Response({"status_code": 200, "data": True})
      return Response({"error": "Attendance record not found"}, status=404)
    except Lecture.DoesNotExist:
      return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def clear_lecture(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      lecture_id = request.data.get("lecture_id")
      lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
      Attendance.objects.filter(lecture_field=lecture_obj).delete()
      return Response({"status_code": 200, "data": True})
    except Lecture.DoesNotExist:
      return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)
