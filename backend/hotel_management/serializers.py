from rest_framework import serializers

from booking.serializers import BookingModelSerializer
from .models import Hotel, Room, Location


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class RoomModelSerializer(serializers.ModelSerializer):
    booking_set = BookingModelSerializer(read_only=True, many=True)
    is_available_status = serializers.Field(source="is_available_status")

    class Meta:
        model = Room
        fields = [
            "room_number",
            "prise_per_day",
            "phone_number",
            "hotel",
            "booking_set",
            "is_available_status",
        ]


class HotelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
