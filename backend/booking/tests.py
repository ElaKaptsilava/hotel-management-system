import datetime

from django.forms import model_to_dict
from django.urls import reverse
from hotel_management.factories import (
    HotelFactory,
    LocationFactory,
    RoomFactory,
    UserFactory,
)
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import BookingFactory


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.admin = UserFactory.create(password="kjbafg873ghdsas9881", is_staff=True)
        self.user = UserFactory.create(password="kjbafg873ghdsas9881")
        self.hotel = HotelFactory.create(location=LocationFactory.create())
        self.room = RoomFactory.create(hotel=self.hotel)
        self.room2 = RoomFactory.create(hotel=self.hotel)
        self.build_booking = BookingFactory.build(
            user=self.admin,
            check_in=datetime.date.today(),
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

        existing_booking_check_in = datetime.date.today()
        existing_booking_check_out = existing_booking_check_in + datetime.timedelta(
            days=3
        )  # Adjust as needed

        BookingFactory.create(
            user=self.admin,
            check_in=existing_booking_check_in,
            check_out=existing_booking_check_out,
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

        self.assertEqual(post_booking.data["detail"], expected_message)

    def test_update_booking_room_as_admin(self):
        self.client.login(username=self.admin.username, password="kjbafg873ghdsas9881")
        booking = BookingFactory.create(
            user=self.admin,
            room=self.room,
        )

        put_booking = self.client.patch(
            reverse("booking-management:bookings-detail", kwargs={"pk": booking.pk}),
            data={"room": self.room2.pk},
            format="json",
        )

        self.assertEqual(put_booking.status_code, status.HTTP_200_OK)
        self.assertEqual(put_booking.data["room"], self.room2.pk)

    def test_delete_booking_as_user_forbidden(self):
        self.client.login(username=self.user.username, password="kjbafg873ghdsas9881")

        booking = BookingFactory.create(
            user=self.admin,
            room=self.room,
        )

        put_booking = self.client.delete(
            reverse("booking-management:bookings-detail", kwargs={"pk": booking.pk}),
            format="json",
        )

        self.assertEqual(put_booking.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_booking_if_user_owner(self):
        self.client.force_login(self.user)

        booking = BookingFactory.create(
            user=self.user,
            room=self.room,
        )
        put_booking = self.client.delete(
            reverse("booking-management:bookings-detail", kwargs={"pk": booking.pk}),
            format="json",
        )
        self.assertEqual(put_booking.status_code, status.HTTP_204_NO_CONTENT)
