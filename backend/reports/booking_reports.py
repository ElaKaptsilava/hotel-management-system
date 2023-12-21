import heapq
from collections import Counter
from dataclasses import dataclass
from datetime import date

from django.db import models
from django.utils import duration, timezone
from phone_iso3166.country import phone_country, network_country

from booking.models import Booking
from hotel_management.models import Hotel


@dataclass
class BookingReport:
    """Data class represents a single booking's report"""

    hotel_name: str
    count_booking: int
    avg_duration: duration
    popular_countries: str
    amount_of_occupied: int
    generated: date


class BookingReportGenerate:
    @classmethod
    def generate_booking_report(cls, instance_hotel):
        repr_booking_reports = cls.get_booking_queryset_to_repr(instance_hotel)
        report = BookingReport(**repr_booking_reports)
        return report

    @classmethod
    def get_booking_queryset_to_repr(cls, instance_hotel):
        booking_queryset = Booking.objects.filter(
            room__hotel__pk=instance_hotel.pk, check_in__month=timezone.now().month
        )
        popular_countries = cls.find_the_most_popular_countries_which_booking(
            booking_queryset
        )
        booking_report_to_repr = cls.get_booking_aggregate(booking_queryset)
        booking_report_to_repr.update(
            {
                "generated": timezone.now(),
                "hotel_name": instance_hotel.name,
                "popular_countries": popular_countries,
            }
        )
        return booking_report_to_repr

    @classmethod
    def get_booking_aggregate(cls, booking_queryset):
        aggregate_queryset = booking_queryset.aggregate(
            count_booking=models.Count("pk"),
            avg_duration=models.Avg("duration"),
        )
        amount_of_occupied = booking_queryset.filter(
            models.Q(
                check_in__lte=timezone.now(),
                check_out__gt=timezone.now(),
            )
        )
        aggregate_queryset.update({"amount_of_occupied": amount_of_occupied.count()})
        aggregate_queryset["avg_duration"] //= 86400
        return aggregate_queryset

    @staticmethod
    def find_the_most_popular_countries_which_booking(booking_queryset):
        phone_queryset = booking_queryset.filter(phone__isnull=False).values_list(
            "phone"
        )
        if phone_queryset.exists():
            booking_countries = [phone_country(phone) for phone in phone_queryset]
            countries_occurs = Counter(booking_countries)
            popular_country = heapq.nlargest(
                1, countries_occurs, key=countries_occurs.get
            )
            return popular_country[0]
        return None
