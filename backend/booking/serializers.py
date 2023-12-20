from django.db import transaction
from rest_framework import serializers

from hotel_management.models import Room
from .models import Booking
from .room_locking import RoomLocking


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

    @transaction.atomic
    def create(self, validated_data):
        RoomLocking.is_available(valid_data=validated_data)
        return Booking.objects.create(**validated_data)
