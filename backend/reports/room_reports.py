from dataclasses import dataclass
from datetime import date

from django.db import models
from django.utils import timezone


@dataclass
class RoomReportRepr:
    """Data class represents a single room's report"""

    hotel: int
    room: int
    amount_of_booking: int
    avg_rate: float
    next_arrival: date


class RoomReportGenerate:
    @classmethod
    def room_report(cls, hotel):
        rooms_instance = hotel.room_set.all()
        reports = []
        for room in cls.get_room_queryset(rooms_instance=rooms_instance):
            report = RoomReportRepr(
                hotel.id,
                room.id,
                room.amount_of_booking,
                room.avg_rate if room.avg_rate is not None else 0,
                room.next_arrival,
            )
            reports.append(report.__dict__)
        return reports

    @staticmethod
    def get_room_queryset(rooms_instance):
        room_queryset = rooms_instance.prefetch_related(
            "booking_set", "review"
        ).annotate(
            amount_of_booking=models.Count("booking"),
            avg_rate=models.Avg("review"),
            next_arrival=models.Case(
                models.When(
                    booking__check_in__gte=timezone.now(),
                    then=models.F("booking__check_in"),
                ),
                default=None,
                output_field=models.DateField(),
            ),
        )
        return room_queryset
