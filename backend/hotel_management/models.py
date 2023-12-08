from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Hotel(ModelsManager):
    name = models.CharField(max_length=250)
    location = models.OneToOneField("Location", on_delete=models.CASCADE)
    description = models.TextField()


class Location(ModelsManager):
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    state = models.CharField(max_length=250)


class Room(ModelsManager):
    class Status(models.TextChoices):
        available = "Available"
        not_available = "NotAvailable"
        reserved = "Reserved"
        occupied = "Occupied"

    room_number = models.IntegerField(unique=True)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.available
    )
    prise_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    phone_number = PhoneNumberField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
