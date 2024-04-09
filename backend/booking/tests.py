from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from django.forms import model_to_dict

from hotel_management.factories import (
    RoomFactory,
    LocationFactory,
    HotelFactory,
    UserFactory,
)
from .factories import BookingFactory


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.admin = UserFactory.create(password="kjbafg873ghdsas9881", is_staff=True)
        self.hotel = HotelFactory.create(location=LocationFactory.create())
        self.room = RoomFactory.create(hotel=self.hotel)
        self.build_booking = BookingFactory.build(
            user=self.admin,
            check_in=datetime.date(year=2024, month=4, day=7),
            room=self.room,
        )

    def test_booking_status_is_active(self):
        self.client.login(username=self.admin.username, password="kjbafg873ghdsas9881")

        post_booking = self.client.post(
            reverse("booking-management:bookings-list"),
            model_to_dict(self.build_booking),
            format="json",
        )

        self.assertEqual(post_booking.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_booking.data["is_active_status"])

    def test_booking_is_not_available(self):
        self.client.login(username=self.admin.username, password="kjbafg873ghdsas9881")
        booking = BookingFactory.create(
            user=self.admin,
            check_in=datetime.date(year=2024, month=4, day=7),
            room=self.room,
        )

        post_booking = self.client.post(
            reverse("booking-management:bookings-list"),
            model_to_dict(self.build_booking),
            format="json",
        )

        expected_message = (
            f"This room is occupied from {self.build_booking.check_in} "
            f"to {self.build_booking.check_out}.You should choose another date"
        )
        print(expected_message)
        self.assertEqual(post_booking.data["detail"], expected_message)
