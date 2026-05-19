"""
URL configuration for TrueFace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from attendance.views import AttendanceViewSet
from authentication.views import HealthView, LoginView
from course.views import CourseViewSet
from lecture.views import LectureViewSet
from students.views import StudentViewSet
from users.views import UserViewSet

# Legacy Admin Router
legacy_router = SimpleRouter()
legacy_router.register(r"students", StudentViewSet)
legacy_router.register(r"courses", CourseViewSet)
legacy_router.register(r"users", UserViewSet)
legacy_router.register(r"lectures", LectureViewSet)

# Legacy Admin Custom Paths
admin_legacy_patterns = [
  path("login", LoginView.as_view()),
  # Students legacy endpoints
  path("students/get_all", StudentViewSet.as_view({"get": "list"})),
  path("students/insert", StudentViewSet.as_view({"post": "insert_legacy"})),
  path("students/update", StudentViewSet.as_view({"post": "update_legacy"})),
  path("students/remove", StudentViewSet.as_view({"post": "destroy_legacy"})),
  path("students/add_lecture", StudentViewSet.as_view({"post": "add_lecture_legacy"})),
  path("students/remove_lecture", StudentViewSet.as_view({"post": "remove_lecture_legacy"})),
  path("students/get_lectures", StudentViewSet.as_view({"get": "get_lectures_legacy"})),
  # Courses legacy endpoints
  path("courses/get_all", CourseViewSet.as_view({"get": "list"})),
  path("courses/insert", CourseViewSet.as_view({"post": "insert_legacy"})),
  path("courses/update", CourseViewSet.as_view({"post": "update_legacy"})),
  path("courses/remove", CourseViewSet.as_view({"post": "destroy_legacy"})),
  path("courses/get_lectures", CourseViewSet.as_view({"get": "get_lectures_legacy"})),
  # Users legacy endpoints
  path("users/get_all", UserViewSet.as_view({"get": "list"})),
  path("users/insert", UserViewSet.as_view({"post": "insert_legacy"})),
  path("users/update", UserViewSet.as_view({"post": "update_legacy"})),
  path("users/remove", UserViewSet.as_view({"post": "destroy_legacy"})),
  # Lectures legacy endpoints
  path("lectures/insert", LectureViewSet.as_view({"post": "insert_legacy"})),
  path("lectures/remove", LectureViewSet.as_view({"post": "destroy_legacy"})),
  path("lectures/update", LectureViewSet.as_view({"post": "update_legacy"})),
]

# Legacy Teacher URLs
teacher_legacy_patterns = [
  path("", HealthView.as_view()),
  path("attendance/insert", AttendanceViewSet.as_view({"post": "insert"})),
  path("attendance/batch_insert", AttendanceViewSet.as_view({"post": "insert"})),
  path("attendance/delete", AttendanceViewSet.as_view({"post": "delete_attendance"})),
  path("attendance/clear_lecture", AttendanceViewSet.as_view({"post": "clear_lecture"})),
  path("lectures/get_by_teacher", LectureViewSet.as_view({"get": "get_by_teacher"})),
  path("lectures/delete", LectureViewSet.as_view({"post": "delete_lecture"})),
  path("lectures/clear_data", LectureViewSet.as_view({"post": "clear_data"})),
  path("students/get_by_lecture", StudentViewSet.as_view({"get": "get_by_lecture"})),
  path("students/remove_from_lecture", StudentViewSet.as_view({"post": "remove_from_lecture"})),
  path("students/clear_attendance", StudentViewSet.as_view({"post": "clear_attendance"})),
]

urlpatterns = [
  path("django-admin/", admin.site.urls),
  path("admin/", include(admin_legacy_patterns)),
  path("admin/", include(legacy_router.urls)),
  path("teacher/", include(teacher_legacy_patterns)),
  path("courses/", include("course.urls")),
  path("users/", include("users.urls")),
  path("lectures/", include("lecture.urls")),
  path("attendances/", include("attendance.urls")),
  path("auth/", include("authentication.urls")),
  path("students/", include("students.urls")),
]
