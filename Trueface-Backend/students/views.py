from datetime import date

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance
from authentication.utils import validate_token
from lecture.models import Lecture, LectureStudentRelation
from students.models import Student
from students.pagination import CustomPagination
from students.serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  pagination_class = CustomPagination
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(create_date=date.today())

  # --- Admin Schedule Actions ---

  @action(detail=True, methods=["get"])
  def lectures(self, request, pk=None):
    relations = LectureStudentRelation.objects.filter(student_id=pk).select_related("lecture_field")

    data = [
      {
        "id": r.lecture_field.id,
        "subject_area": r.lecture_field.subject_area,
        "start_time": r.lecture_field.start_time,
        "end_time": r.lecture_field.end_time,
        "day": r.day,
      }
      for r in relations
    ]

    return Response(data)

  @action(detail=True, methods=["post"])
  def add_lecture(self, request, pk=None):
    LectureStudentRelation.objects.create(
      id=request.data.get("relation_id"),
      student_id=pk,
      lecture_field_id=request.data["lecture_id"],
      day=request.data["day"],
    )
    return Response({"success": True})

  @action(detail=True, methods=["delete"])
  def remove_lecture(self, request, pk=None):
    LectureStudentRelation.objects.filter(
      student_id=pk, lecture_field_id=request.data["lecture_id"], day=request.data["day"]
    ).delete()
    return Response({"success": True})

  # --- Teacher Dashboard Actions ---

  @action(detail=False, methods=["get"])
  def get_by_lecture(self, request):
    current_lecture = request.query_params.get("current_lecture")
    today_name = date.today().strftime("%A")
    today_date = date.today().isoformat()

    relations = (
      LectureStudentRelation.objects.filter(lecture_field_id=current_lecture, day=today_name)
      .select_related("student")
      .prefetch_related("student__attendance_set")
    )

    attendance_records = {
      att.student_id: att.time.strftime("%H:%M")
      for att in Attendance.objects.filter(lecture_field_id=current_lecture, date=today_date).select_related("student")
    }

    data = []
    for relation in relations:
      student = relation.student
      data.append(
        {
          "id": student.id,
          "first_name": student.first_name,
          "middle_name": student.middle_name,
          "last_name": student.last_name,
          "gender": student.gender,
          "face_id": student.face_id,
          "time": attendance_records.get(student.id),
        }
      )
    return Response(data)

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def remove_from_lecture(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      student_id = request.data.get("student_id")
      lecture_id = request.data.get("lecture_id")
      day = request.data.get("day")

      try:
        lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)

        Attendance.objects.filter(student_id=student_id, lecture_field=lecture_obj).delete()

        relation = LectureStudentRelation.objects.filter(
          student_id=student_id, lecture_field=lecture_obj, day=day
        ).first()

        if relation:
          relation.delete()
          return Response({"success": True})
        return Response({"error": "Student not found in this lecture"}, status=404)
      except Lecture.DoesNotExist:
        return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)

  @action(detail=False, methods=["post"])
  @transaction.atomic
  def clear_attendance(self, request):
    try:
      current_teacher = validate_token(request.data.get("current_teacher")).get("user_id")
      student_id = request.data.get("student_id")
      lecture_id = request.data.get("lecture_id")

      try:
        lecture_obj = Lecture.objects.get(id=lecture_id, instructor_id=current_teacher)
        attendance_count = Attendance.objects.filter(student_id=student_id, lecture_field=lecture_obj).count()

        if attendance_count > 0:
          Attendance.objects.filter(student_id=student_id, lecture_field=lecture_obj).delete()
          return Response({"success": True})
        return Response({"error": "No attendance records found"}, status=404)
      except Lecture.DoesNotExist:
        return Response({"error": "Lecture not found or access denied"}, status=404)
    except Exception as e:
      return Response({"error": str(e)}, status=500)
