from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet

router = DefaultRouter()
router.register(r"", CourseViewSet)

urlpatterns = router.urls
