import datetime
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from django.db import models
from django.utils import timezone


@dataclass
class RoomReportRepr:
    """Data class represents a single room's report"""

    is_available: bool

    hotel_name: int
    room_number: int

    count_rate: int
    avg_rate: Decimal

    amount_of_booking: int

    next_arrival: date
    generated: datetime


class RoomReportGenerate:
    @classmethod
    def generate_room_report(cls, room_instance):
        review_aggregate = cls.get_review_aggregate(room_instance)
        booking_aggregate = cls.get_booking_aggregate(room_instance)
        complete_report = {
            "hotel_name": room_instance.hotel.name,
            "room_number": room_instance.room_number,
            "is_available": room_instance.is_available_status,
            "generated": timezone.now(),
        }
        complete_report.update(booking_aggregate)
        complete_report.update(review_aggregate)
        room_report = RoomReportRepr(**complete_report)
        return room_report

    @staticmethod
    def get_review_aggregate(room_instance):
        review_aggregate = room_instance.review.aggregate(
            avg_rate=models.Avg("rate"),
            count_rate=models.Count("id"),
        )
        return review_aggregate

    @staticmethod
    def get_booking_aggregate(room_instance):
        booking_aggregate = room_instance.booking_set.aggregate(
            amount_of_booking=models.Count("id"),
        )
        next_arrival = (
            room_instance.booking_set.filter(models.Q(check_in__gte=timezone.now()))
            .order_by("check_in")
            .first()
        )
        booking_aggregate.update(
            {
                "next_arrival": next_arrival.check_in
                if next_arrival is not None
                else None
            }
        )
        return booking_aggregate
