from rest_framework.routers import DefaultRouter

from lecture.views import LectureViewSet

router = DefaultRouter()
router.register(r"", LectureViewSet)

urlpatterns = router.urls
