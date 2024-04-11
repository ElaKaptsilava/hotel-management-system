from hotel_management.models import Room
from rest_framework import serializers


class RoomInitialModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "room_number",
            "hotel",
            "prise_per_day",
            "phone_number",
        ]


class RoomReportSerializer(serializers.Serializer):
    is_available = serializers.BooleanField()

    hotel_name = serializers.CharField(max_length=256)
    room_number = serializers.IntegerField()

    count_rate = serializers.IntegerField()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

    amount_of_booking = serializers.IntegerField()
    next_arrival = serializers.DateField(allow_null=True)
    generated = serializers.DateTimeField()


class HotelReportSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=256)

    number_of_ratings_for_hotel = serializers.IntegerField()
    hotel_rating: serializers.FloatField()
    hotel_occupancy_percentage = serializers.IntegerField()

    count_rooms = serializers.IntegerField()
    rooms_rating = serializers.IntegerField()
    number_of_ratings_for_rooms = serializers.IntegerField()
    amount_of_occupied = serializers.IntegerField()
    count_discounts = serializers.IntegerField()

    generated = serializers.DateTimeField()


class BookingReportSerializer(serializers.Serializer):
    hotel = serializers.CharField(max_length=256)
    count_booking = serializers.IntegerField()
    avg_duration = serializers.FloatField()
    popular_countries = serializers.CharField(max_length=256, allow_null=True)
    amount_of_occupied = serializers.IntegerField()
    generated = serializers.DateTimeField()


class RoomsPageReportSerializer(serializers.Serializer):
    room_amount = serializers.IntegerField()

    count_rate = serializers.IntegerField()
    avg_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

    generated = serializers.DateTimeField()
