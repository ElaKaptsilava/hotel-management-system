from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hotel_management.models import Location, Hotel, Room
from .models import Booking
from .room_locking import RoomLocking


class BookingApiTestCase(APITestCase):
    def setUp(self):
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
            prise_per_day=80.00,
            phone_number="+48713589849",
            hotel=self.create_hotel,
        )
        self.booking = {
            "user": self.create_admin.id,
            "check_in": datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            "check_out": datetime.strptime("2023-12-13", "%Y-%m-%d").date(),
            "room": self.create_room.id,
        }

        self.bookings_list_url = reverse("bookings-management:bookings-list")
        self.rooms_detail_url = reverse(
            "hotel-management:rooms-detail", kwargs={"pk": self.create_room.id}
        )

    def test_should_return_True_when_is_available_dates(self):
        is_available_dates = RoomLocking.is_available_dates(
            room=self.create_room, valid_data=self.booking
        )

        self.assertTrue(is_available_dates)

    def test_should_return_generated_token(self):
        self.client.login(username="root", password="1234")

        post_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )
        self.assertEqual(post_token.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in post_token.json())

    def test_should_return_created_object_for_authenticated_user(self):
        self.client.login(username="root", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        post_booking = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )
        get_room = self.client.get(self.rooms_detail_url, format="json")

        self.assertEqual(post_booking.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_room.json().get("status"), "Reserved")

    def test_create_booking_for_user(self):
        self.client.login(username="user", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        post_bookings = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )

        self.assertEqual(post_bookings.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_bookings.json().get("status"), "Reserved")

    def test_user_create_booking_with_occupied_date(
        self,
    ):
        self.client.login(username="user", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        booking = {
            "user": self.create_admin.id,
            "check_in": datetime.strptime("2023-12-06", "%Y-%m-%d").date(),
            "check_out": datetime.strptime("2023-12-10", "%Y-%m-%d").date(),
            "room": self.create_room.id,
        }

        post_booking_1 = self.client.post(
            self.bookings_list_url, booking, format="json"
        )
        post_booking_2 = self.client.post(
            self.bookings_list_url, self.booking, format="json"
        )

        self.assertEqual(
            post_booking_2.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_should_return_no_content_when_destroy_booking_for_authenticated_admin(
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

    def test_should_return_403_when_destroy_booking_for_authenticated_user(self):
        self.client.login(username="user", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
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

        self.assertEqual(destroy_booking.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Booking.objects.filter(id=create_booking.id).exists())
        self.assertEqual(
            destroy_booking.json()["detail"],
            "You do not have permission to perform this action.",
        )
