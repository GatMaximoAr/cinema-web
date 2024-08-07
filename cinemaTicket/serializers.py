from rest_framework import serializers
from .models import CinemaRoom, Projection
from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CinemaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaRoom
        fields = ("id", "name", "capacity")


class ProjectionSerializer(WritableNestedModelSerializer):
    cinema_rooms = CinemaRoomSerializer(many=True, required=False)

    class Meta:
        model = Projection
        fields = ("id", "projection_date", "start_time", "created_at", "cinema_rooms")
        read_only_fields = ("created_at",)
        depth = 1
