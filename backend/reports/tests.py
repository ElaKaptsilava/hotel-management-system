from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Booking
from hotel_management.models import Location, Hotel, Room
from .room_reports import RoomReportGenerate
from .booking_reports import BookingReportGenerate
from .hotel_reports import HotelReportGenerate


class ReportApiTestCase(APITestCase):
    def setUp(self):
        self.create_admin = User.objects.create_superuser(
            username="root", password="1234", email="root@gmail.com"
        )

        self.create_location = Location.objects.create(
            city="city", country="country", street="street", state="state"
        )
        self.create_hotel = Hotel.objects.create(
            name="hotel", location=self.create_location, description="About hotel."
        )
        self.create_room = Room.objects.create(
            room_number=1,
            prise_per_day=80.00,
            phone_number="+48713589849",
            hotel=self.create_hotel,
        )
        self.create_room_2 = Room.objects.create(
            room_number=2,
            prise_per_day=80.00,
            phone_number="+48713589849",
            hotel=self.create_hotel,
        )

        self.create_booking = Booking.objects.create(
            user=self.create_admin,
            check_in="2023-12-06",
            check_out="2023-12-13",
            room=self.create_room,
            phone="+48713589849",
        )
        self.create_booking_2 = Booking.objects.create(
            user=self.create_admin,
            check_in="2023-12-15",
            check_out="2023-12-17",
            room=self.create_room,
            phone="+48713589849",
        )
        self.create_booking_3 = Booking.objects.create(
            user=self.create_admin,
            check_in="2023-12-18",
            check_out="2023-12-22",
            room=self.create_room,
            phone="+48713589849",
        )

    def test_generate_booking_reports(self):
        generate = BookingReportGenerate.generate_booking_report("hotel")
        self.assertEqual(generate.popular_countries, "PL")
        self.assertEqual(generate.avg_duration.days, 4)

    def test_generate_hotel_reports(self):
        generate = HotelReportGenerate.hotel_report("hotel")
        self.assertEqual(generate.count_rooms, 4)

    def test_admin_generate_booking_reports(self):
        self.client.login(username="root", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )

        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        get_reports = self.client.post(
            reverse("reports:booking-reports-list", kwargs={"hotel_name": "hotel"}),
            format="json",
        )

        self.assertEqual(get_reports.json(), status.HTTP_201_CREATED)

    def test_admin_generate_hotel_reports(self):
        self.client.login(username="root", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )

        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        get_reports = self.client.post(
            reverse("reports:hotel-reports-list", kwargs={"hotel_name": "hotel"}),
            format="json",
        )

        self.assertEqual(get_reports.json(), status.HTTP_201_CREATED)
