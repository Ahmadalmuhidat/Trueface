from django.contrib import admin

from course.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ["id", "title", "subject_area", "catalog_nbr", "component", "campus"]
  list_filter = ["subject_area", "component", "campus", "academic_group"]
  search_fields = ["id", "title", "subject_area", "catalog_nbr", "academic_organization"]
  ordering = ["id"]
