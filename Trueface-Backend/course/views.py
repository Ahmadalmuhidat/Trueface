from rest_framework import viewsets
from rest_framework.response import Response

from course.models import Course
from course.pagination import CustomPagination
from course.serializers import CourseSerializer
from lecture.models import Lecture


class CourseViewSet(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  pagination_class = CustomPagination

  from rest_framework.decorators import action

  @action(detail=True, methods=["get"])
  def lectures(self, request, pk=None):
    lectures = Lecture.objects.filter(course_id=pk).select_related("instructor")
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
    return Response(data)
