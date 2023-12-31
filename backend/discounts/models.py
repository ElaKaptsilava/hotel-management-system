import datetime

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

    generated = models.DateField(default=datetime.date.today())
    expiration_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        if self.percentage_value:
            return f"{self.percentage_value}%"
        return f"{self.value}$"

    def __repr__(self):
        class_name = type(self).__name__
        if self.percentage_value:
            return f"{class_name}(pk={self.pk!r},percentage_value {self.percentage_value!r})"
        return f"{class_name}(pk={self.pk!r},value {self.value!r})"
