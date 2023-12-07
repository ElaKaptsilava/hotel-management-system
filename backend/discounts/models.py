from django.db import models
from hotel_management import models as hotel_models


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Discount(ModelsManager):
    value = models.IntegerField()
    is_percentage = models.BooleanField(default=True)
    rooms = models.ManyToManyField(hotel_models.Room, default=list)

    def __str__(self):
        if self.is_percentage:
            return f"{self.value}%"
        return f"{self.value}$"
