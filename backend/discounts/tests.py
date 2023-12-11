from django.urls import reverse
from rest_framework.test import APITestCase

from hotel_management.models import Location, Hotel, Room
from .discount_counter import DiscountCounter
from .models import Discount


class DiscountCounterAPITestCase(APITestCase):
    def setUp(self):
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
        self.discount = Discount.objects.create(value=10, is_percent=True)
        self.discount.rooms.set(self.create_room)

    def test_changing_price_per_day_with_discount(self):
        url = reverse("discount-management:rooms-list")

        discount = self.client.post(url, content, format="json")
