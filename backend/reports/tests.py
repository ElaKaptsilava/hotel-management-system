import datetime

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.factories import BookingFactory
from booking.models import Booking
from hotel_management.factories import (
    HotelFactory,
    LocationFactory,
    RoomFactory,
    UserFactory,
)
from hotel_management.models import Hotel, Room
from reports.paginations import RoomResultsSetPagination
from reviews.factories import AbstractReviewFactory


class ReportsApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(password="cu7eq923GK")
        self.admin = UserFactory.create(password="lxm712HJKHK", is_staff=True)

        self.hotel1 = HotelFactory.create(user=self.user, location=LocationFactory())

        self.room1 = RoomFactory.create(hotel=self.hotel1)
        self.room2 = RoomFactory.create(hotel=self.hotel1)
        self.room3 = RoomFactory.create(hotel=self.hotel1)

        self.content_type_hotel = ContentType.objects.get_for_model(Hotel)
        self.content_type_room = ContentType.objects.get_for_model(Room)

        self.build_booking = BookingFactory.create(
            user=self.admin,
            check_in=datetime.date(year=2024, month=4, day=7),
            room=self.room1,
        )
        self.build_booking = BookingFactory.create(
            user=self.admin,
            check_in=datetime.date(year=2024, month=4, day=7),
            room=self.room2,
        )

        self.hotel_rates = self.generate_reviews(
            self.hotel1, self.content_type_hotel, 5
        )
        self.room_rates = self.generate_reviews(self.room1, self.content_type_room, 5)

    @staticmethod
    def generate_reviews(object, content_type, n):
        hotel_rates = []
        for _ in range(n):
            user = UserFactory.create()
            abstract_review = AbstractReviewFactory.create(
                user=user, content_type=content_type, object_id=object.pk
            )
            hotel_rates.append(abstract_review.rate)
        return hotel_rates

    def test_hotel_report_generation(self):
        self.client.login(username=self.admin.username, password="lxm712HJKHK")

        get_report = self.client.get(
            reverse("reports:hotels-hotel-reports", kwargs={"pk": self.hotel1.pk}),
            format="json",
        )

        self.assertEqual(get_report.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_report.data["hotel_name"], self.hotel1.name)
        self.assertEqual(
            get_report.data["hotel_rating"],
            sum(self.hotel_rates) / len(self.hotel_rates),
        )
        self.assertEqual(
            get_report.data["rooms_rating"], sum(self.room_rates) / len(self.room_rates)
        )

    def test_booking_reports_generation(self):
        self.client.login(username=self.admin.username, password="lxm712HJKHK")

        get_report = self.client.get(
            reverse("reports:hotels-booking-reports", kwargs={"pk": self.hotel1.pk}),
            format="json",
        )

        self.assertEqual(get_report.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            get_report.data["count_booking"],
            Booking.objects.filter(room__hotel__name=self.hotel1.name).count(),
        )

    def test_rooms_report_generation(self):
        self.client.login(username=self.admin.username, password="lxm712HJKHK")

        get_report = self.client.get(
            reverse("reports:hotels-get-rooms", kwargs={"pk": self.hotel1.pk}),
            format="json",
        )

        self.assertEqual(get_report.status_code, status.HTTP_201_CREATED)

    def test_get_page_room_reports(self):
        self.client.login(username=self.admin.username, password="lxm712HJKHK")

        for _ in range(30):
            RoomFactory.create(hotel=self.hotel1)

        get_report = self.client.get(
            reverse("reports:rooms-page-reports"), format="json"
        )

        self.assertEqual(get_report.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            get_report.data["room_amount"], RoomResultsSetPagination.page_size
        )

    def test_retrieve_room_report_generation(self):
        self.client.login(username=self.admin.username, password="lxm712HJKHK")

        get_report = self.client.get(
            reverse("reports:rooms-detail", kwargs={"pk": self.room1.pk}), format="json"
        )

        self.assertEqual(get_report.status_code, status.HTTP_201_CREATED)

    def test_forbidden_report_generation(self):
        self.client.login(username=self.user.username, password="cu7eq923GK")

        get_report = self.client.get(
            reverse("reports:rooms-detail", kwargs={"pk": self.room1.pk}), format="json"
        )

        self.assertEqual(get_report.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_room_report_generation_retrieve(self):
        get_report = self.client.get(
            reverse("reports:rooms-detail", kwargs={"pk": self.room1.pk}), format="json"
        )

        self.assertEqual(get_report.status_code, status.HTTP_401_UNAUTHORIZED)
