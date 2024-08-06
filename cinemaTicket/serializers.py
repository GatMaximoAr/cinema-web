from rest_framework import serializers
from .models import CinemaRoom, Projection
from django.core.exceptions import ObjectDoesNotExist


class CinemaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaRoom
        fields = ("id", "name", "capacity")


class ProjectionSerializer(serializers.ModelSerializer):
    cinema_rooms = CinemaRoomSerializer(many=True, allow_null=True)

    class Meta:
        model = Projection
        fields = ("id", "projection_date", "start_time", "created_at", "cinema_rooms")
        read_only_fields = ("created_at",)
        depth = 1

    def create(self, validated_data):
        rooms_data = validated_data.pop("cinema_rooms")
        projection = Projection.objects.create(**validated_data)

        if rooms_data is not None:
            for room_data in rooms_data:
                try:
                    room = CinemaRoom.objects.get(name=room_data["name"])
                    projection.cinema_rooms.add(room)
                except ObjectDoesNotExist as error:
                    print("error throw in query database: " + type(error).__name__)

        return projection

    def update(self, instance, validated_data):

        instance.projection_date = validated_data.get(
            "projection_date", instance.projection_date
        )
        instance.start_time = validated_data.get("start_time", instance.start_time)

        rooms_data = validated_data.pop("cinema_rooms")

        if rooms_data is not None:
            instance.cinema_rooms.set([])
            for room_data in rooms_data:
                try:
                    room = CinemaRoom.objects.get(name=room_data["name"])
                    instance.cinema_rooms.add(room)
                except ObjectDoesNotExist as error:
                    print("error throw in query database: " + type(error).__name__)
        else:
            instance.cinema_rooms.set([])

        return instance
