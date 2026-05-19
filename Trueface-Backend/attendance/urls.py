from rest_framework.routers import DefaultRouter

from attendance.views import AttendanceViewSet

router = DefaultRouter()
router.register(r"", AttendanceViewSet)

urlpatterns = router.urls
