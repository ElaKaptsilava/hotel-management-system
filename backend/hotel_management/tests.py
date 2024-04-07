from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.factories import BookingFactory
from booking.serializers import BookingModelSerializer
from .serializers import RoomModelSerializer
from hotel_management.factories import RoomFactory, UserFactory, HotelFactory, LocationFactory


class HotelManagementAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(password='12345678dsad', is_staff=True)
        self.hotel = HotelFactory.create(user=self.user, location=LocationFactory.create())
        self.room = RoomFactory.build(hotel=self.hotel)
        self.booking = BookingFactory.build(room=self.room, user=self.user)

    def test_is_available_room(self):
        self.client.login(username=self.user.username, password='12345678dsad')

        room_serializer = RoomModelSerializer(self.room)
        post_room = self.client.post(reverse('hotel-management:rooms-list'), data=room_serializer.data, format='json')

        self.assertEqual(post_room.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_room.data['is_available_status'], True)
