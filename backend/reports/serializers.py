from rest_framework import serializers

from hotel_management.serializers import HotelModelSerializer, RoomModelSerializer


class RoomReportModelSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=256)
    room_number = serializers.IntegerField()
    amount_of_booking = serializers.IntegerField()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    next_arrival = serializers.DateField(allow_null=True)


class HotelReportModelSerializer(serializers.Serializer):
    hotel = HotelModelSerializer()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    count_rooms = serializers.IntegerField()
    amount_of_reserved = serializers.IntegerField()
    amount_of_available = serializers.IntegerField()
    hotel_occupancy_percentage = serializers.IntegerField()


class BookingReportModelSerializer(serializers.Serializer):
    hotel = HotelModelSerializer()
    room = RoomModelSerializer()
    arrival = serializers.DateField()
    check_out = serializers.DateField()
