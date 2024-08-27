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
    cinema_rooms = CinemaRoomSerializer(many=True, required=False)
    movie = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Movie.objects.all()
    )
    projection_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Projection
        fields = "__all__"
        read_only_fields = ("created_at",)
        depth = 1


class TicketSerializer(WritableNestedModelSerializer):
    projection = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Projection.objects.all()
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        depth = 1
