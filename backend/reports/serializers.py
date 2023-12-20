from rest_framework import serializers

from hotel_management.models import Hotel
from reports.models import HotelReport, RoomReport, BookingReport


class RoomReportInitialModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReport
        fields = "__all__"
        read_only_fields = [
            "id",
            "room",
            "avg_rate",
            "amount_of_booking",
            "next_arrival",
            "generated",
        ]


class RoomReportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReport
        fields = "__all__"
        read_only_fields = ["generated"]


class HotelInitialModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReport
        fields = "__all__"
        read_only_fields = [
            "id",
            "avg_rate",
            "count_rooms",
            "amount_of_occupied",
            "hotel_occupancy_percentage",
            "count_discounts",
            "generated",
        ]

    def validate(self, data):
        hotel_name = data.get("hotel_name")
        if not Hotel.objects.filter(name=hotel_name):
            raise serializers.ValidationError("The hotel doesn't exist yet.")
        return data


class HotelReportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReport
        fields = "__all__"
        read_only_fields = ["generated", "hotel_occupancy_percentage"]


class BookingReportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingReport
        fields = "__all__"
        read_only_fields = ["generated"]


class BookingReportInitialModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingReport
        fields = "__all__"
        read_only_fields = [
            "count_booking",
            "avg_duration",
            "popular_countries",
            "amount_of_occupied",
            "generated",
        ]
