from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Booking
from hotel_management.models import Location, Hotel, Room
from .reports_generation import HotelReportGenerate, RoomReportGenerate


class ReportApiTestCase(APITestCase):
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
        )

    def test_room_report(self):
        self.client.login(username="root", password="1234")

        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )

        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        get_reports = self.client.post(
            reverse("reports-api:room-reports-list"),
            kwargs={"hotel": self.create_hotel},
            format="json",
        )
        print(get_reports)
        print(get_reports.json())
        self.assertEqual(get_reports.json(), get_reports)

    # def test_should_return_403_for_authenticated_user(self):
    #     self.client.login(username="user", password="1234")
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "user", "password": "1234"}, format="json"
    #     )
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.get(reverse("reports:hotel-reports"), format="json")
    #
    #     self.assertEqual(
    #         get_reports.json()["detail"],
    #         "You do not have permission to perform this action.",
    #     )
    #     self.assertEqual(get_reports.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_should_return_reports_for_authenticated_admin(self):
    #     self.client.login(username="root", password="1234")
    #     create_token = self.client.post(
    #         reverse("token"), {"username": "root", "password": "1234"}, format="json"
    #     )
    #     access = create_token.json()["access"]
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    #
    #     get_reports = self.client.get(reverse("reports:hotel-reports"))
    #     get_hotel = self.client.get(
    #         reverse(
    #             "hotel-management:hotels-detail", kwargs={"pk": self.create_hotel.id}
    #         )
    #     )
    #
    #     required = [
    #         {
    #             "hotel": get_hotel.json(),
    #             "avg_rate": None,
    #             "count_rooms": 1,
    #             "amount_of_reserved": 0,
    #             "amount_of_available": 1,
    #             "hotel_occupancy_percentage": 0,
    #         }
    #     ]
    #
    #     self.assertEqual(get_reports.json(), required)
    #     self.assertEqual(get_reports.status_code, status.HTTP_201_CREATED)
