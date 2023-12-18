from datetime import timedelta

from django.db import models
from django.db.models import Count, Avg, Q
from django.utils import timezone

from booking.models import Booking
from hotel_management.models import Hotel, Room
from reports.reports_representation import HotelReport, RoomReport, BookingReport


class RoomReportGenerate:
    @classmethod
    def room_report(cls):
        reports = [
            RoomReport(
                room.hotel.name,
                room.room_number,
                room.amount_of_booking,
                room.avg_rate,
                room.next_arrival,
            )
            for room in cls.get_user_queryset()
        ]
        return reports

    @staticmethod
    def get_user_queryset():
        room_select_related = Room.objects.prefetch_related(
            "booking_set", "hotel", "review"
        )
        room_queryset = room_select_related.annotate(
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
    def hotel_report(cls):
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
        select_booking = filter_booking_gte_now.select_related("room__hotel")
        return select_booking