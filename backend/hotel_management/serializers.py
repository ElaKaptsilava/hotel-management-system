from rest_framework import serializers

from .models import Hotel, Room, Location


class HotelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
