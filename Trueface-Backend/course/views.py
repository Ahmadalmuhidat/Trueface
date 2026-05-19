from rest_framework import viewsets
from rest_framework.response import Response

from course.models import Course
from course.serializers import CourseSerializer
from lecture.models import Lecture
from students.views import CustomPagination


class CourseViewSet(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  pagination_class = CustomPagination

  # --- Legacy Desktop App Mappings ---

  def insert_legacy(self, request):
    data = request.data.copy()
    data["id"] = request.data.get("course_id")
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status_code": 200, "data": True})

  def update_legacy(self, request):
    course_id = request.data.get("course_id")
    course = Course.objects.get(id=course_id)
    data = request.data.copy()
    data["id"] = course_id
    serializer = self.get_serializer(course, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status_code": 200, "data": True})

  def destroy_legacy(self, request):
    course_id = request.data.get("course_id")
    Course.objects.filter(id=course_id).delete()
    return Response({"status_code": 200, "data": True})

  def get_lectures_legacy(self, request):
    course_id = request.query_params.get("course_id")
    lectures = Lecture.objects.filter(course_id=course_id).select_related("instructor")
    data = [
      {
        "id": lec.id,
        "subject_area": lec.subject_area,
        "catalog_nbr": lec.catalog_nbr,
        "academic_career": lec.academic_career,
        "course": lec.course_id,
        "offering_nbr": lec.offering_nbr,
        "start_time": lec.start_time.strftime("%H:%M:%S") if lec.start_time else None,
        "end_time": lec.end_time.strftime("%H:%M:%S") if lec.end_time else None,
        "section": lec.section,
        "component": lec.component,
        "campus": lec.campus,
        "instructor": lec.instructor.name if lec.instructor else None,
      }
      for lec in lectures
    ]
    return Response({"status_code": 200, "data": data})
