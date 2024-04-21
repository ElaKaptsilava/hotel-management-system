from django.db import models, transaction
from hotel_management.models import Room
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Booking


class BookingModelSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = [
            "id",
            "is_active_status",
            "user",
            "check_in",
            "check_out",
            "room",
            "duration",
            "phone",
        ]

    def validate(self, data: dict) -> dict:
        room = data.get("room")
        check_in = data.get("check_in")
        check_out = data.get("check_out")

        if check_in and check_out:
            first_condition = models.Q(check_in__lte=check_in, check_out__gt=check_in)
            second_condition = models.Q(
                check_in__lt=check_out, check_out__gte=check_out
            )

            is_available = room.booking_set.filter(
                first_condition | second_condition
            ).exists()
        else:
            is_available = False

        if is_available:
            raise APIException(
                f"This room is occupied from {data.get('check_in')} to {data.get('check_out')}."
                f"You should choose another date"
            )
        if not room:
            raise APIException("Room is required.")
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> Booking:
        return Booking.objects.create(**validated_data)
