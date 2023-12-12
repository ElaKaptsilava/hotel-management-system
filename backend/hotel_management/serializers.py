from rest_framework import serializers

from .models import Hotel, Room, Location


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class HotelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class HotelReportModelSerializer(serializers.Serializer):
    hotel = HotelModelSerializer()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    count_rooms = serializers.IntegerField()
    amount_of_reserved = serializers.IntegerField()
    amount_of_available = serializers.IntegerField()
    hotel_occupancy_percentage = serializers.IntegerField()
