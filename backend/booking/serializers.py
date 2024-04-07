from django.db import transaction, models
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Booking


class BookingModelSerializer(serializers.ModelSerializer):
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
        ]

    def validate(self, data: dict) -> dict:
        room = data.get("room")
        is_available = room.booking_set.filter(
            models.Q(
                check_in__lte=data.get("check_in"),
                check_out__gt=data.get("check_in"),
            )
            or models.Q(
                check_in__lt=data.get("check_out"),
                check_out__gte=data.get("check_out"),
            )
        ).exists()
        if is_available:
            raise APIException(
                f"This room is occupied from {data.get('check_in')} to {data.get('check_out')}."
                f"You should choose another date"
            )
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> Booking:
        return Booking.objects.create(**validated_data)
