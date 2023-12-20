from datetime import timedelta

from django.db import models
from django.db.models import Count, Avg, Q
from django.utils import timezone

from booking.models import Booking
from hotel_management.models import Hotel, Room
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
    def booking_report(cls):
        reports = [
            BookingReport(
                booking.room.hotel, booking.room, booking.check_in, booking.check_out
            )
            for booking in cls.get_booking_queryset()
        ]
        return reports

    @staticmethod
    def get_booking_queryset():
        filter_booking_gte_now = Booking.objects.filter(
            models.Q(check_in__gte=timezone.now())
            & models.Q(check_in__lte=timezone.now() + timedelta(days=7))
        )
        select_booking = filter_booking_gte_now.select_related("room__hotel").annotate
        return select_booking
