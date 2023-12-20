import heapq
from collections import Counter
from datetime import timedelta

from django.db import models
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from phone_iso3166.country import phone_country

from hotel_management.models import Hotel
from reports.reports_representation import (
    RoomReportRepr,
    BookingReport,
    HotelReportRepr,
)


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
        print(reports)
        return reports

    @staticmethod
    def get_room_queryset(rooms_instance):
        room_queryset = rooms_instance.prefetch_related(
            "booking_set", "review"
        ).annotate(
            amount_of_booking=Count("booking"),
            avg_rate=Avg("review"),
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
                count_rooms=Count("room"),
                avg_rate=Avg("review__rate"),
                amount_of_occupied=Count(
                    "room",
                    filter=Q(
                        room__booking__check_in__lte=timezone.now(),
                        room__booking__check_out__gt=timezone.now(),
                    ),
                ),
                count_discounts=Count(
                    "room__discount",
                    filter=Q(room__discount__generated__month=timezone.now().month),
                ),
            )
        )
        return hotel_queryset


class BookingReportGenerate:
    @classmethod
    def generate_booking_report(cls, hotel_name):
        repr_booking_reports = cls.get_booking_queryset_to_repr(hotel_name)
        repr_booking_reports.update({"hotel_name": hotel_name})
        reports = BookingReport(**repr_booking_reports)
        return reports

    @classmethod
    def get_booking_queryset_to_repr(cls, hotel_name):
        get_hotel = Hotel.objects.get(name=hotel_name)
        booking_queryset = get_hotel.room_set.prefetch_related("booking_set").filter(
            models.Q(booking__check_in__gte=timezone.now())
            & models.Q(booking__check_in__lte=timezone.now() - timedelta(days=7))
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
            count_booking=Count("booking"),
            avg_duration=Avg("booking__duration"),
            amount_of_occupied=Count(
                "booking",
                filter=Q(
                    booking__check_in__lte=timezone.now(),
                    booking__check_out__gt=timezone.now(),
                ),
            ),
        )
        return aggregate_queryset

    @staticmethod
    def find_the_most_popular_countries_which_booking(queryset):
        booking_phones = list(
            queryset.exclude(**{"phone_number": None})
            .values_list("phone_number", flat=True)
            .distinct()
        )
        booking_countries = [
            phone_country(phone.country_code) for phone in booking_phones
        ]
        countries_occurs = Counter(booking_countries)
        popular_country = heapq.nlargest(1, countries_occurs, key=countries_occurs.get)
        return {
            "popular_countries": popular_country[0]
            if len(popular_country) != 0
            else None
        }
