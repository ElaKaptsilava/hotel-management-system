from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Booking
from hotel_management.models import Location, Hotel, Room

from .booking_reports import BookingReportGenerate
from .hotel_reports import HotelReportGenerate
from .room_reports import RoomReportGenerate


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
        self.create_location_hotel2 = Location.objects.create(
            city="city2", country="country2", street="street2", state="state2"
        )
        self.create_hotel_2 = Hotel.objects.create(
            name="hotel2",
            location=self.create_location_hotel2,
            description="About hotel2.",
        )
        self.create_room_hotel2 = Room.objects.create(
            room_number=5,
            prise_per_day=100.00,
            phone_number="+48713589849",
            hotel=self.create_hotel_2,
        )

        self.create_booking_hotel2 = Booking.objects.create(
            user=self.create_admin,
            check_in="2023-12-29",
            check_out="2023-12-30",
            room=self.create_room_hotel2,
        )

    # def test_generate_booking_reports(self):
    #     generate = BookingReportGenerate.generate_booking_report("hotel")
    #     self.assertEqual(generate.popular_countries, "PL")
    #     self.assertEqual(generate.avg_duration.days, 4)

    def test_generate_hotel_report(self):
        generate_hotel_report = HotelReportGenerate.generate_hotel_report(
            self.create_hotel
        )
        self.assertEqual(generate_hotel_report.count_rooms, 2)

    def test_generate_room_report(self):
        generate_room_report = RoomReportGenerate.generate_room_report(
            self.create_room_hotel2
        )
        self.assertFalse(generate_room_report.is_available)
        self.assertEqual(generate_room_report.next_arrival.__str__(), "2023-12-29")

    def test_generate_booking_report(self):
        generate_booking_report = BookingReportGenerate.generate_booking_report(
            self.create_hotel
        )
        self.assertEqual(generate_booking_report.avg_duration.days, 4)
        self.assertEqual(generate_booking_report.avg_duration.days, 4)
        self.assertEqual(generate_booking_report.popular_countries, "PL")

    # def test_admin_generate_booking_reports(self):
    #     self.client.login(username="root", password="1234")
    #
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "root", "password": "1234"}, format="json"
    #     )
    #
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.post(
    #         reverse("reports:booking-reports-list"),
    #         {"hotel_name": "hotel"},
    #         format="json",
    #     )
    #
    #     self.assertEqual(get_reports.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(get_reports.json()["amount_of_occupied"], 1)
    #
    # def test_admin_generate_hotel_reports(self):
    #     self.client.login(username="root", password="1234")
    #
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "root", "password": "1234"}, format="json"
    #     )
    #
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.post(
    #         reverse("reports:hotel-reports-list"),
    #         {"hotel_name": "hotel"},
    #         format="json",
    #     )
    #
    #     self.assertEqual(get_reports.status_code, status.HTTP_201_CREATED)
    #
    # def test_admin_generate_booking_reports_when_booking_without_phone_number(self):
    #     self.client.login(username="root", password="1234")
    #
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "root", "password": "1234"}, format="json"
    #     )
    #
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.post(
    #         reverse("reports:booking-reports-list"),
    #         {"hotel_name": "hotel2"},
    #         format="json",
    #     )
    #
    #     self.assertEqual(get_reports.status_code, status.HTTP_201_CREATED)
    #     self.assertIsNone(get_reports.json()["popular_countries"])
    #
    # def test_admin_generate_room_reports(self):
    #     self.client.login(username="root", password="1234")
    #
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "root", "password": "1234"}, format="json"
    #     )
    #
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.post(
    #         reverse("reports:room-reports-list"),
    #         {"hotel": self.create_hotel.pk},
    #         format="json",
    #     )
    #     print(get_reports.json())
    #
    #     self.assertEqual(get_reports.status_code, status.HTTP_201_CREATED)
