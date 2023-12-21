import heapq
from collections import Counter
from dataclasses import dataclass

from django.db import models
from django.utils import duration, timezone
from phone_iso3166.country import phone_country

from hotel_management.models import Hotel


@dataclass
class BookingReport:
    """Data class represents a single booking's report"""

    hotel_name: str
    count_booking: int
    avg_duration: duration
    popular_countries: str
    amount_of_occupied: int


class BookingReportGenerate:
    @classmethod
    def generate_booking_report(cls, hotel_name):
        repr_booking_reports = cls.get_booking_queryset_to_repr(hotel_name)
        repr_booking_reports.update({"hotel_name": hotel_name})
        report = BookingReport(**repr_booking_reports)
        return report

    @classmethod
    def get_booking_queryset_to_repr(cls, hotel_name):
        get_hotel = Hotel.objects.get(name=hotel_name)
        booking_queryset = get_hotel.room_set.prefetch_related("booking_set").filter(
            models.Q(booking__check_in__month=timezone.now().month)
        )
        popular_countries = cls.find_the_most_popular_countries_which_booking(
            queryset=booking_queryset
        )
        booking_report_to_repr = cls.get_aggregate_queryset(queryset=booking_queryset)
        booking_report_to_repr.update(popular_countries)
        return booking_report_to_repr

    @classmethod
    def get_aggregate_queryset(cls, queryset):
        aggregate_queryset = queryset.aggregate(
            count_booking=models.Count("booking"),
            avg_duration=models.Avg("booking__duration"),
            amount_of_occupied=models.Count(
                "booking",
                filter=models.Q(
                    booking__check_in__lte=timezone.now(),
                    booking__check_out__gt=timezone.now(),
                ),
            ),
        )
        return aggregate_queryset

    @staticmethod
    def find_the_most_popular_countries_which_booking(queryset):
        booking_countries = list()
        for room in queryset:
            phone = (
                room.booking_set.exclude(**{"phone": None})
                .values_list("phone", flat=True)
                .distinct()
            )
            if phone.exists():
                booking_countries.append(phone_country(phone))
        countries_occurs = Counter(booking_countries)
        popular_country = heapq.nlargest(1, countries_occurs, key=countries_occurs.get)
        return {
            "popular_countries": popular_country[0]
            if len(popular_country) != 0
            else None
        }
