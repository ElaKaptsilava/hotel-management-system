import json

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from hotel_management import models as hotel_models


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.location1 = hotel_models.Location.objects.create(city='city', country='country1', street='street',
                                                              state='state')
        self.hotel1 = hotel_models.Hotel.objects.create(name='hotel1', location=self.location1,
                                                        description='About hotel1.')
        self.room1 = hotel_models.Room.objects.create(room_number=1, prise_per_day=1.00, phone_number='+48713589849',
                                                      hotel=self.hotel1)

    def test_created_reservation(self):
        self.self_client = self.client(reverse('bookings:bookings-users-list'), json.dumps(
            {"check_in": '05/12/2023', "check_out": '06/12/2023', "room": self.room1}),
                                       content_type="application/json")
        response = self.self_client

        self.assertEqual(response.data, '')
