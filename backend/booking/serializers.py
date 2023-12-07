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
        is_reserved_room = room_locking.is_available(valid_data=data)
        if not is_reserved_room:
            return serializers.ValidationError(
                f"This room is occupied from {data.get('check_in')} to {data.get('check_out')}."
                f"You should choose another date"
            )
        return data

    def create(self, validated_data):
        return Booking.objects.create(
            status="Reserved",
            check_in=validated_data.get("check_in"),
            check_out=validated_data.get("check_out"),
            room=validated_data.get("room"),
        )
