from rest_framework import serializers
from .models import CinemaRoom


class CinemaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaRoom
        fields = ("id", "name", "capacity")
