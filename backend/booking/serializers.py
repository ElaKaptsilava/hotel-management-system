from rest_framework import serializers

from .models import Booking
from .room_locking import RoomLocking


class BookingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["status"]

    def validate(self, data):
        room_locking = RoomLocking()
        reserved_room = room_locking.is_available(room=data.get("room"))
        if not reserved_room:
            return serializers.ValidationError("This room already occupied.")
        return data

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
