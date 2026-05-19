from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

from authentication.utils import cache_invalidate, generate_password
from users.pagination import CustomPagination
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  pagination_class = CustomPagination

  def list(self, request):
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 100)

    cache_key = f"users_{page}_{page_size}"

    cached = cache.get(cache_key)
    if cached:
      return Response(cached)

    page = self.paginate_queryset(self.get_queryset())

    serializer = self.get_serializer(page, many=True)
    response = self.get_paginated_response(serializer.data)

    cache.set(cache_key, response.data, 300)

    return response

  def perform_create(self, serializer):
    serializer.save(password=make_password(generate_password()))
    cache_invalidate("users_*")

  def perform_update(self, serializer):
    serializer.save()
    cache_invalidate("users_*")

  def perform_destroy(self, instance):
    instance.delete()
    cache_invalidate("users_*")

  # --- Legacy Desktop App Mappings ---

  def insert_legacy(self, request):
    data = request.data.copy()
    data["id"] = request.data.get("user_id")
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response({"status_code": 200, "data": True})

  def update_legacy(self, request):
    user_id = request.data.get("user_id")
    user = User.objects.get(id=user_id)
    data = request.data.copy()
    data["id"] = user_id
    serializer = self.get_serializer(user, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response({"status_code": 200, "data": True})

  def destroy_legacy(self, request):
    user_id = request.data.get("user_id")
    User.objects.filter(id=user_id).delete()
    cache_invalidate("users_*")
    return Response({"status_code": 200, "data": True})
