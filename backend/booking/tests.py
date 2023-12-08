import json

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from hotel_management.models import Location, Hotel, Room


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.location1 = Location.objects.create(
            city="city", country="country1", street="street", state="state"
        )
        self.hotel1 = Hotel.objects.create(
            name="hotel1", location=self.location1, description="About hotel1."
        )
        self.room1 = Room.objects.create(
            room_number=1,
            prise_per_day=1.00,
            phone_number="+48713589849",
            hotel=self.hotel1,
        )

    def test_created_reservation(self):
        booking = self.client.post(
            "/bookings/bookings-users/",
            json.dumps(
                {
                    "check_in": "2023-12-06",
                    "check_out": "2023-12-08",
                    "room": self.room1,
                }
            ),
            content_type="application/json",
        )
        response = booking

        self.assertEqual(response.json(), "")
