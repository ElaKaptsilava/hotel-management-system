from django.urls import reverse
from hotel_management.factories import (
    HotelFactory,
    LocationFactory,
    RoomFactory,
    UserFactory,
)
from hotel_management.models import Room
from rest_framework import status
from rest_framework.test import APITestCase


class DiscountCounterAPITestCase(APITestCase):
    def setUp(self):
        self.admin = UserFactory.create(password="12345678dsad", is_staff=True)
        self.hotel = HotelFactory.create(
            user=self.admin, location=LocationFactory.create()
        )
        self.room = RoomFactory.create(hotel=self.hotel)
        self.room1 = RoomFactory.create(hotel=self.hotel, prise_per_day=5)
        self.value = 10

    def test_adjusting_room_price_after_applying_discount(self):
        self.client.login(username=self.admin.username, password="12345678dsad")
        discount_dict = {"value": self.value, "rooms": [self.room.id]}

        post_discount = self.client.post(
            reverse("discounts-management:discounts-list"), discount_dict, format="json"
        )
        get_room = Room.objects.get(id=self.room.id)

        self.assertEqual(post_discount.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.room.prise_per_day - self.value, get_room.prise_per_day)

    def test_adjusting_room_price_after_applying_discount_with_percentage(self):
        self.client.login(username=self.admin.username, password="12345678dsad")
        discount_dict = {"percentage_value": self.value, "rooms": [self.room.id]}

        post_discount = self.client.post(
            reverse("discounts-management:discounts-list"), discount_dict, format="json"
        )
        get_room = Room.objects.get(id=self.room.id)
        expected = round(self.room.prise_per_day * (100 - self.value) / 100, 2)

        self.assertEqual(post_discount.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected, get_room.prise_per_day)

    def test_adjusting_room_price_after_applying_discount_value_greate_then_price(self):
        self.client.login(username=self.admin.username, password="12345678dsad")
        discount_dict = {"value": self.value, "rooms": [self.room1.id]}

        post_discount = self.client.post(
            reverse("discounts-management:discounts-list"), discount_dict, format="json"
        )

        self.assertEqual(
            post_discount.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(post_discount.data["detail"], "Price cannot be less than 0")
