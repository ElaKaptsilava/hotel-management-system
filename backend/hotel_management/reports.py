"""This code generates a hotel report by calculating various statistics related to hotels and their rooms."""

from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Count, Avg, Q

from hotel_management.models import Hotel, Room


@dataclass
class HotelReport:
    """Data class represents a single hotel's report"""

    hotel: Hotel
    avg_rate: Decimal
    count_rooms: int
    amount_of_reserved: int
    amount_of_available: int
    hotel_occupancy_percentage: int


class HotelReportGenerate:
    @classmethod
    def hotel_report(cls):
        """
        Retrieves data for all hotels and computes the required statistics.

        Returns:
            list: A list of HotelReport objects containing hotel information."""
        reports = [
            HotelReport(
                hotel,
                hotel.avg_rate,
                hotel.count_rooms,
                hotel.amount_of_reserved,
                hotel.amount_of_available,
                hotel_occupancy_percentage=round(
                    (hotel.amount_of_reserved * 100) / hotel.count_rooms
                ),
            )
            for hotel in cls.get_hotel_queryset()
        ]
        return reports

    @staticmethod
    def get_hotel_queryset():
        """
        Retrieves the hotel queryset with additional annotations.
        Returns:
            QuerySet: An annotated queryset containing hotel data."""
        hotel_queryset = Hotel.objects.all().annotate(
            count_rooms=Count("room"),
            avg_rate=Avg("review__rate"),
            amount_of_reserved=Count(
                "room", filter=Q(room__status__exact=Room.Status.reserved)
            ),
            amount_of_available=Count(
                "room", filter=Q(room__status__exact=Room.Status.available)
            ),
        )
        return hotel_queryset
