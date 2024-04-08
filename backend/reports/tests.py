from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hotel_management.factories import HotelFactory, RoomFactory, LocationFactory, UserFactory
from discounts.factories import DiscountFactory
from booking.factories import BookingFactory


class ReportApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(password='cu7eq923GK')
        self.admin = UserFactory.create(password='lxm712HJKHK', is_staff=True)

        self.hotel1 = HotelFactory.create(user=self.user, location=LocationFactory())
        self.hotel2 = HotelFactory.create(user=self.user, location=LocationFactory())

        self.room1 = RoomFactory.create(hotel=self.hotel1)
        self.room2 = RoomFactory.create(hotel=self.hotel1)
        self.room3 = RoomFactory.create(hotel=self.hotel1)

        self.room4 = RoomFactory.create(hotel=self.hotel2)
        self.room5 = RoomFactory.create(hotel=self.hotel2)
        self.room6 = RoomFactory.create(hotel=self.hotel2)
        self.room7 = RoomFactory.create(hotel=self.hotel2)

    def test_hotel_report(self):
        get_report = self.client.get(reverse('reports:hotels'), format='json')
        print(get_report)
