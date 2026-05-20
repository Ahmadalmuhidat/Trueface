from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

from authentication.utils import cache_invalidate, generate_password
from users.models import User
from users.pagination import CustomPagination
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
