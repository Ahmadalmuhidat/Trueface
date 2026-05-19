from django.contrib import admin

from lecture.models import Lecture, LectureStudentRelation


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
  list_display = [
    "id",
    "subject_area",
    "catalog_nbr",
    "section",
    "component",
    "course",
    "instructor",
    "start_time",
    "end_time",
  ]
  list_filter = ["subject_area", "component", "campus", "academic_career", "course", "instructor"]
  search_fields = ["id", "subject_area", "catalog_nbr", "section", "instructor__name"]
  ordering = ["id"]


@admin.register(LectureStudentRelation)
class LectureStudentRelationAdmin(admin.ModelAdmin):
  list_display = ["id", "student", "lecture_field", "day"]
  list_filter = ["day", "lecture_field"]
  search_fields = ["student__first_name", "student__last_name", "student__id", "lecture_field__id"]
  ordering = ["lecture_field", "student"]
