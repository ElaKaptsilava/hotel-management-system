from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from hotel_management import models as hotel_models


class Review(models.Model):
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=256)
    comment = models.TextField()
    objects = models.Manager()

    class Meta:
        abstract = True


class HotelReview(Review):
    hotel = models.ForeignKey(hotel_models.Hotel, on_delete=models.CASCADE)


class RoomReview(Review):
    room = models.ForeignKey(hotel_models.Room, on_delete=models.CASCADE)
