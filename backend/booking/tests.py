from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APITestCase

from hotel_management.models import Location, Hotel, Room
from .room_locking import RoomLocking


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.bookings_list_url = reverse("bookings-management:bookings-list")

        self.create_admin = User.objects.create_superuser(
            username="root", password="1234", email="root@gmail.com"
        )
        self.create_user = User.objects.create_user(
            username="user", password="1234", email="root@gmail.com"
        )
        self.location = {
            "city": "city",
            "country": "country1",
            "street": "street",
            "state": "state",
        }

        self.create_location = Location.objects.create(**self.location)
        self.create_hotel = Hotel.objects.create(
            name="name", location=self.create_location, description="About hotel."
        )
        self.create_room = Room.objects.create(
            room_number=1,
            prise_per_day=100.00,
            phone_number="+48713589849",
            hotel=self.create_hotel,
        )
        self.booking = {
            "user": self.create_admin.id,
            "check_in": datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            "check_out": datetime.strptime("2023-12-13", "%Y-%m-%d").date(),
            "room": self.create_room.id,
        }

    def test_should_return_True_when_dates_is_available_dates(self):
        booking = {
            "user": self.create_admin.id,
            "check_in": datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            "check_out": datetime.strptime("2023-12-10", "%Y-%m-%d").date(),
            "room": self.create_room.id,
        }

        is_available_dates = RoomLocking.is_available_dates(
            room=self.create_room, valid_data=booking
        )

        self.assertTrue(is_available_dates)

    def test_should_return_created_object_when_admin_create_booking(self):
        self.client.login(username="root", password="1234")

        request_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )
        self.assertEqual(request_token.status_code, status.HTTP_200_OK)

        rooms_detail_url = reverse(
            "hotel-management:rooms-detail", kwargs={"pk": self.create_room.id}
        )

        request = self.client.post(self.bookings_list_url, self.booking, format="json")
        request_rooms = self.client.get(rooms_detail_url, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request_rooms.json().get("status"), "Reserved")

    def test_when_user_create_booking_with_token_jwt(self):
        self.client.login(username="user", password="1234")

        request_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )

        self.assertEqual(request_token.status_code, status.HTTP_200_OK)

        request_bookings = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )

        self.assertEqual(request_bookings.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request_bookings.json().get("status"), "Reserved")

    def test_user_create_booking_with_occupied_date(
        self,
    ):
        booking = {
            "user": self.create_admin.id,
            "check_in": datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            "check_out": datetime.strptime("2023-12-10", "%Y-%m-%d").date(),
            "room": self.create_room,
        }

        self.client.login(username="user", password="1234")

        request_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )
        send_booking_1 = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )

        send_booking_2 = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )

        self.assertEqual(
            send_booking_2.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
