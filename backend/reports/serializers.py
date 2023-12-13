from rest_framework import serializers

from hotel_management.serializers import HotelModelSerializer


class HotelReportModelSerializer(serializers.Serializer):
    hotel = HotelModelSerializer()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    count_rooms = serializers.IntegerField()
    amount_of_reserved = serializers.IntegerField()
    amount_of_available = serializers.IntegerField()
    hotel_occupancy_percentage = serializers.IntegerField()
