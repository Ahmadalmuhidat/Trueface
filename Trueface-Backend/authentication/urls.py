from django.urls import path

from authentication.views import HealthView, LoginView

urlpatterns = [
  path("login/", LoginView.as_view(), name="login"),
  path("health/", HealthView.as_view(), name="health"),
]
