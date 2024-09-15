from rest_framework import serializers
from cinemaTicket.models import *
from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CinemaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaRoom
        fields = "__all__"


class MovieSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"
        depth = 1


class ProjectionSerializer(WritableNestedModelSerializer):
    cinema_room = serializers.PrimaryKeyRelatedField(
        required=True, queryset=CinemaRoom.objects.all()
    )

    movie = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Movie.objects.all()
    )

    projection_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Projection
        fields = "__all__"
        read_only_fields = ("created_at",)
        depth = 1


class ValidEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValidEmail
        fields = ("id", "email", "is_verified", "otp_expires_at", "otp_code")
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if "otp_code" in representation:
            representation.pop("otp_code")

        return representation


class TicketSerializer(WritableNestedModelSerializer):
    projection = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Projection.objects.all()
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        depth = 1

    def validate(self, attrs):
        room_capacity = attrs["projection"].cinema_room.capacity
        tickets_spended = Ticket.objects.filter(projection=attrs["projection"]).count()
        # print(room_capacity)
        # print(tickets_spended)

        if tickets_spended < room_capacity:
            return attrs
        else:
            raise serializers.ValidationError("the current projection is soul out")
