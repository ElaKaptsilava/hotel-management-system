import datetime
from dataclasses import dataclass

from django.db import models
from django.utils import timezone

from hotel_management.models import Hotel


@dataclass
class HotelReportRepr:
    """Data class represents a single hotel's report"""

    hotel_name: str

    number_of_ratings_for_hotel: int
    hotel_rating: float
    hotel_occupancy_percentage: int

    count_rooms: int
    rooms_rating: float
    number_of_ratings_for_rooms: int
    amount_of_occupied: int
    count_discounts: int

    generated: datetime


class HotelReportGenerate:
    @classmethod
    def generate_hotel_report(cls, instance_hotel: Hotel) -> HotelReportRepr:
        instance_rooms = instance_hotel.room_set
        rooms_queryset = cls.get_room_queryset(instance_rooms)
        amount_of_occupied_room = cls.get_amount_of_occupied_room(instance_rooms)
        hotel_queryset = cls.get_hotel_queryset(instance_hotel)
        complete_report = {
            "hotel_name": instance_hotel.name,
            "amount_of_occupied": amount_of_occupied_room,
            "hotel_occupancy_percentage": round(
                amount_of_occupied_room * 100 / rooms_queryset.get("count_rooms")
            ),
            "generated": timezone.now(),
        }
        complete_report.update(hotel_queryset)
        complete_report.update(rooms_queryset)
        reports = HotelReportRepr(**complete_report)
        return reports

    @staticmethod
    def get_room_queryset(instance_rooms: models.QuerySet) -> dict:
        room_queryset = instance_rooms.prefetch_related(
            "discount_set", "review"
        ).aggregate(
            count_rooms=models.Count("id"),
            number_of_ratings_for_rooms=models.Count("review"),
            rooms_rating=models.Avg("review__rate"),
            count_discounts=models.Count(
                "discount",
                filter=models.Q(discount__generated__month=timezone.now().month),
            ),
        )
        return room_queryset

    @staticmethod
    def get_amount_of_occupied_room(instance_rooms: models.QuerySet) -> int:
        filter_by_occupied_room = instance_rooms.filter(
            models.Q(
                booking__check_in__lte=timezone.now(),
                booking__check_out__gt=timezone.now(),
            )
        )
        return filter_by_occupied_room.count()

    @staticmethod
    def get_hotel_queryset(hotel_instance: Hotel) -> models.QuerySet:
        hotel_queryset = hotel_instance.review.aggregate(
            number_of_ratings_for_hotel=models.Count("rate"),
            hotel_rating=models.Avg("rate"),
        )
        return hotel_queryset
