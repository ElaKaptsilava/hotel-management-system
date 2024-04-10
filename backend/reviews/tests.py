from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hotel_management.factories import (HotelFactory, LocationFactory,
                                        RoomFactory, UserFactory)
from hotel_management.models import Hotel

from .factories import AbstractReviewFactory


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.admin = UserFactory.create(password="12345678dsad", is_staff=True)
        self.hotel = HotelFactory.create(
            user=self.admin, location=LocationFactory.create()
        )
        self.room = RoomFactory.create(hotel=self.hotel)
        self.content_type = ContentType.objects.get_for_model(Hotel)
        self.object_id = self.hotel.pk
        self.abstract_review_build = AbstractReviewFactory.build(
            user=self.admin, content_type=self.content_type, object_id=self.object_id
        )

    def test_post_hotel_review_unauthorized_user(self):
        abstract_review = self.abstract_review_build.__dict__
        abstract_review.pop("_state")

        post_review = self.client.post(
            reverse("reviews-management:reviews-list"), abstract_review, format="json"
        )

        self.assertEqual(post_review.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_hotel_review_authorized_user(self):
        self.client.login(username=self.admin.username, password="12345678dsad")

        request = {
            "user": self.admin.pk,
            "object_id": self.object_id,
            "content_type": self.content_type.pk,
            "rate": self.abstract_review_build.rate,
            "title": self.abstract_review_build.title,
            "comment": self.abstract_review_build.comment,
        }

        post_review = self.client.post(
            reverse("reviews-management:reviews-list"), request, format="json"
        )

        self.assertEqual(post_review.status_code, status.HTTP_201_CREATED)
