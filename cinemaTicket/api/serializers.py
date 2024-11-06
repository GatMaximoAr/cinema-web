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


class TicketSerializer(serializers.ModelSerializer):
    projection = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Projection.objects.all()
    )
    email = serializers.SlugRelatedField(
        many=False, queryset=ValidEmail.objects.all(), slug_field="email", required=True
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("validate_code",)
        depth = 1

    def create(self, validated_data):
        # print(validated_data)
        ticket = Ticket(
            email=validated_data["email"],
            customer_name=validated_data["customer_name"],
            projection=validated_data["projection"],
        )
        ticket.save()
        return ticket

    def validate(self, attrs):
        room_capacity = attrs["projection"].cinema_room.capacity
        tickets_spended = Ticket.objects.filter(projection=attrs["projection"]).count()
        email = ValidEmail.objects.get(email=attrs["email"].email)

        if not email.is_verified:
            raise serializers.ValidationError("El email no está validado.")

        elif tickets_spended >= room_capacity:
            raise serializers.ValidationError("the current projection is soul out")
        else:
            return attrs
