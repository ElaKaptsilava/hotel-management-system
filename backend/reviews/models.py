from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from hotel_management.models import Hotel, Room


class Review(models.Model):
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=256)
    comment = models.TextField()
    objects = models.Manager()

    class Meta:
        abstract = True


class HotelReview(Review):
    hotel = models.ForeignKey(Hotel, models.CASCADE)


class RoomReview(Review):
    hotel = models.ForeignKey(Room, models.CASCADE)
