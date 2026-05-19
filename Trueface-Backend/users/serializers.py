from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(required=False, write_only=True)

  class Meta:
    model = User
    fields = "__all__"
