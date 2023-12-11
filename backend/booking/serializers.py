from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException

from hotel_management.models import Room
from hotel_management.serializers import RoomModelSerializer
from .models import Booking
from .room_locking import RoomLocking


class BookingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["status"]

    @transaction.atomic
    def create(self, validated_data):
        is_reserved_room = RoomLocking.is_available(valid_data=validated_data)
        validated_data.get("room").status = Room.Status.reserved
        validated_data.get("room").save()
        return Booking.objects.create(**validated_data)
