from django.db import models
from django.utils import timezone

from hotel_management import models as hotel_models


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Booking(ModelsManager):
    class Status(models.TextChoices):
        reserved = "Reserved"
        canceled = "Canceled"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.reserved
    )
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField(default=timezone.now)
    room = models.ForeignKey(hotel_models.Room, on_delete=models.CASCADE)
