from django.db import models
from django.utils import timezone
from hotel_management import models as hotel_models


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Discount(ModelsManager):
    value = models.PositiveIntegerField(
        null=True, blank=True, help_text="Discount value"
    )
    percentage_value = models.PositiveIntegerField(
        null=True, blank=True, help_text="Discount percentage value"
    )
    rooms = models.ManyToManyField(
        hotel_models.Room, default=list, help_text="Discount rooms"
    )

    generated = models.DateField(default=timezone.now)
    expiration_date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        if self.percentage_value:
            return f"{self.percentage_value} %"
        return f"{self.value} $"

    def __repr__(self) -> str:
        class_name = type(self).__name__
        if self.percentage_value:
            return f"{class_name}(pk={self.pk!r},percentage_value {self.percentage_value!r})"
        return f"{class_name}(pk={self.pk!r},value {self.value!r})"
