import datetime

from booking.factories import BookingFactory
from django.urls import reverse
from hotel_management.factories import (
    HotelFactory,
    LocationFactory,
    RoomFactory,
    UserFactory,
)
from rest_framework import status
from rest_framework.test import APITestCase


class HotelManagementAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(password="12345678dsad", is_staff=True)
        self.hotel = HotelFactory.create(
            user=self.user, location=LocationFactory.create()
        )
        self.room = RoomFactory.create(hotel=self.hotel)

    def test_room_is_available(self):
        self.client.login(username=self.user.username, password="12345678dsad")

        get_room = self.client.get(
            reverse("hotel-management:rooms-detail", kwargs={"pk": self.room.pk}),
            format="json",
        )

        self.assertEqual(get_room.status_code, status.HTTP_200_OK)
        self.assertEqual(get_room.data["is_available_status"], True)

    def test_room_unavailable_after_booking(self):
        self.client.login(username=self.user.username, password="12345678dsad")

        booking = BookingFactory.create(
            check_in=datetime.date(year=2024, month=4, day=6),
            room=self.room,
            user=self.user,
        )

        self.assertFalse(booking.room.is_available_status)
