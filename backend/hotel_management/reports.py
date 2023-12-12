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


def hotel_report():
    """The function retrieves data for all hotels and computes the required statistics"""
    data = []
    queryset = Hotel.objects.all().annotate(
        count_rooms=Count("room"),
        avg_rate=Avg("review__rate"),
        amount_of_reserved=Count("room", filter=Q(room__status=Room.Status.reserved)),
    )
    for hotel in queryset.values():
        hotel_query = Hotel.objects.get(pk=hotel["id"])
        report = HotelReport(
            hotel_query,
            hotel["avg_rate"],
            hotel["count_rooms"],
            hotel["amount_of_reserved"],
        )
        data.append(report)
    return data
