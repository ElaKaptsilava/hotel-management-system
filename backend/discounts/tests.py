from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError

from booking.tests import BookingApiTestCase
from .discount_counter import DiscountCounter


class DiscountCounterAPITestCase(BookingApiTestCase):
    def test_changing_price_with_percentage_value(self):
        discount_percentage = {
            "percentage_value": 20,
            "rooms": [self.create_room],
        }

        DiscountCounter.is_percentage(discount_percentage)
        self.assertEqual(self.create_room.prise_per_day, 64)

    def test_changing_price_with_currency(self):
        discount_percentage = {
            "value": 20,
            "rooms": [self.create_room],
        }

        DiscountCounter.is_percentage(discount_percentage)
        self.assertEqual(self.create_room.prise_per_day, 60)

    def test_should_return_ValidationError_when_changing_price_with_currency(self):
        discount_percentage = {
            "value": 100,
            "rooms": [self.create_room],
        }

        with self.assertRaises(ValidationError):
            DiscountCounter.is_percentage(discount_percentage)

    def test_should_return_created_discounts_when_admin_set_discounts(
        self,
    ):
        self.client.login(username="root", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "root", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        discount = {
            "value": 20,
            "percentage_value": None,
            "rooms": [self.create_room.id],
        }

        discounts_list_url = reverse("discounts-management:discounts-list")
        set_discount = self.client.post(discounts_list_url, discount, format="json")
        set_discount.json().pop("id")

        self.assertEqual(set_discount.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set_discount.json(), discount)

    def test_should_return_403_when_user_set_discounts(
        self,
    ):
        self.client.login(username="user", password="1234")
        create_token = self.client.post(
            reverse("token"), {"username": "user", "password": "1234"}, format="json"
        )
        access = create_token.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        discount = {
            "value": 20,
            "rooms": [self.create_room.id],
        }

        discounts_list_url = reverse("discounts-management:discounts-list")
        set_discount = self.client.post(discounts_list_url, discount, format="json")

        self.assertEqual(set_discount.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            set_discount.json()["detail"],
            "You do not have permission to perform this action.",
        )
