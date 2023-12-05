import uuid

from rest_framework import serializers

from .models import Booking
from .room_locking import RoomLocking


class BookingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status', 'reservation_id']

    def validate(self, data):
        room_locking = RoomLocking()
        reserved_room = room_locking.is_available(room=data.get('rooms'))
        if not reserved_room:
            return serializers.ValidationError('This room already occupied.')
        return data

    def create(self, validated_data):
        reservation_id = uuid.uuid4()
        while Booking.objects.filter(reservation_id=reservation_id):
            reservation_id = uuid.uuid4()
        return Booking.objects.create(reservation_id=reservation_id,
                                      status='Reserved',
                                      check_in=validated_data.get('check_in'),
                                      check_out=validated_data.get('check_out'),
                                      rooms=validated_data.get('rooms'))
