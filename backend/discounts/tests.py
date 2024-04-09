from django.forms import model_to_dict
from django.urls import reverse
from rest_framework.test import APITestCase

from discounts.factories import DiscountFactory
from hotel_management.factories import (
    UserFactory,
    HotelFactory,
    RoomFactory,
    LocationFactory,
)
from .discount_counter import DiscountCounter


class DiscountCounterAPITestCase(APITestCase):
    def setUp(self):
        self.admin = UserFactory.create(password="12345678dsad", is_staff=True)
        self.hotel = HotelFactory.create(
            user=self.admin, location=LocationFactory.create()
        )
        self.room = RoomFactory.create(hotel=self.hotel)
        self.build_discount = DiscountFactory.build()

    def test_discount_value(self):
        self.client.login(username=self.admin.username, password="12345678dsad")
        self.build_discount.percentage_value = None
        print(self.room)
        self.build_discount.save()
        self.build_discount.rooms.set([self.room])
        print(self.build_discount.__dict__)
