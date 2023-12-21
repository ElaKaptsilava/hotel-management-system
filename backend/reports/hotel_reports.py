from dataclasses import dataclass

from django.db import models
from django.utils import timezone

from hotel_management.models import Hotel


@dataclass
class HotelReportRepr:
    """Data class represents a single hotel's report"""

    hotel: str
    avg_rate: float
    count_rooms: int
    amount_of_occupied: int
    count_discounts: int


class HotelReportGenerate:
    @classmethod
    def hotel_report(cls, hotel_name):
        hotel = cls.get_hotel_queryset(hotel_name=hotel_name)[0]
        reports = HotelReportRepr(
            hotel.name,
            hotel.avg_rate,
            hotel.count_rooms,
            hotel.amount_of_occupied,
            hotel.count_discounts,
        )
        return reports

    @staticmethod
    def get_hotel_queryset(hotel_name):
        hotel_queryset = (
            Hotel.objects.filter(name=hotel_name)
            .prefetch_related("room_set__discount_set", "review")
            .annotate(
                count_rooms=models.Count("room"),
                avg_rate=models.Avg("review__rate"),
                amount_of_occupied=models.Count(
                    "room",
                    filter=models.Q(
                        room__booking__check_in__lte=timezone.now(),
                        room__booking__check_out__gt=timezone.now(),
                    ),
                ),
                count_discounts=models.Count(
                    "room__discount",
                    filter=models.Q(
                        room__discount__generated__month=timezone.now().month
                    ),
                ),
            )
        )
        return hotel_queryset
