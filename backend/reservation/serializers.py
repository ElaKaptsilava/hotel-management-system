import uuid

from rest_framework import serializers

from .models import Booking
from .room_locking import RoomLocking


class BookingModelSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['duration', 'status', 'reservation_id']

    def validate(self, data):
        room_locking = RoomLocking()
        reserved_room = room_locking.is_available(room=data.get('rooms'))
        if not reserved_room:
            return serializers.ValidationError('This room already occupied.')
        bookings_id = Booking.objects.filter(reservation_id=data.get('reservation_id'))
        while bookings_id.count() > 0:
            data['reservation_id'] = uuid.uuid4()
        return data

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
