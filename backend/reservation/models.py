from django.db import models
import uuid

from hotel_management import models as hotel_models


class Booking(models.Model):
    class Status(models.TextChoices):
        reserved = 'Reserved'
        canceled = 'Canceled'

    reservation_id = models.CharField(max_length=250, default=uuid.uuid4())
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.reserved)
    check_in = models.DateField()
    check_out = models.DateField()
    rooms = models.ForeignKey(hotel_models.Room, on_delete=models.CASCADE)
