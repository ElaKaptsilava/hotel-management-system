from django.db import models
from hotel_management import models as hotel_models


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Discount(ModelsManager):
    value = models.PositiveIntegerField(null=True, blank=True)
    percentage_value = models.PositiveIntegerField(null=True, blank=True)
    rooms = models.ManyToManyField(hotel_models.Room, default=list)

    def __str__(self):
        if self.percentage_value:
            return f"{self.percentage_value}%"
        return f"{self.value}$"
