from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APITestCase

from hotel_management.models import Location, Hotel, Room
from .models import Booking


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.create_admin = User.objects.create_superuser(
            username="root", password="1234", email="root@gmail.com"
        )

        self.create_user = User.objects.create_user(
            username="user", password="1234", email="root@gmail.com"
        )

        self.create_location = Location.objects.create(
            city="city", country="country", street="street", state="state"
        )
        self.create_hotel = Hotel.objects.create(
            name="name", location=self.create_location, description="About hotel."
        )
        self.create_room = Room.objects.create(
            room_number=1,
            prise_per_day=80.00,
            phone_number="+48713589849",
            hotel=self.create_hotel,
        )
        self.create_booking = Booking.objects.create(
            user=self.create_admin,
            check_in="2023-12-06",
            check_out="2023-12-13",
            room=self.create_room,
        )


        self.bookings_list_url = reverse("bookings-management:bookings-list")
        self.rooms_detail_url = reverse(
            "hotel-management:rooms-detail", kwargs={"pk": self.create_room.id}
        )

    def test_should_return_generated_token(self):
        post_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )

        self.assertEqual(post_token.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in post_token.json())

    def test_should_return_created_booking_for_authenticated_user(self):
        self.client.login(username="root", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        booking = {
            "user": self.create_admin.id,
            "check_in": "2023-12-18",
            "check_out": "2023-12-20",
            "room": self.create_room.id,
        }

        post_booking = self.client.post(self.bookings_list_url, booking, format="json")

        get_room = Room.objects.get(id=post_booking.json()["room"])

        self.assertEqual(post_booking.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_booking.json()["is_active_status"])
        self.assertTrue(get_room.is_available_status)

    def test_admin_can_destroy_booking_successful(
            self,
    ):
        self.client.login(username="root", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )

        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        create_booking = Booking.objects.create(
            user=self.create_admin,
            check_in=datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            check_out=datetime.strptime("2023-12-10", "%Y-%m-%d").date(),
            room=self.create_room,
        )

        bookings_detail_url = reverse(
            "bookings-management:bookings-detail", kwargs={"pk": create_booking.id}
        )
        destroy_booking = self.client.delete(bookings_detail_url, format="json")

        self.assertEqual(destroy_booking.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=create_booking.id).exists())

    def test_user_can_not_destroy_booking(self):
        self.client.login(username="user", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )

        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        bookings_detail_url = reverse(
            "bookings-management:bookings-detail", kwargs={"pk": self.create_booking.id}
        )
        destroy_booking = self.client.delete(bookings_detail_url, format="json")

        self.assertEqual(destroy_booking.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Booking.objects.filter(id=self.create_booking.id).exists())
