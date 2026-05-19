from rest_framework import serializers

from lecture.models import Lecture, LectureStudentRelation


class LectureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lecture
    fields = "__all__"


class LectureStudentRelationSerializer(serializers.ModelSerializer):
  class Meta:
    model = LectureStudentRelation
    fields = "__all__"
