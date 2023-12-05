from rest_framework import serializers

from .models import Booking


class BookingModelSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Booking
        field = '__all__'
        read_only_fields = ['duration']
