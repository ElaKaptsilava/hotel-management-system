from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from reviews.models import AbstractReview


class ModelsManager(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Hotel(ModelsManager):
    name = models.CharField(max_length=250)
    location = models.OneToOneField("Location", on_delete=models.CASCADE)
    description = models.TextField()
    review = GenericRelation(AbstractReview)


class Location(ModelsManager):
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    state = models.CharField(max_length=250)


class RoomQuerySet(QuerySet):
    def with_booking(self):
        return self.prefetch_related("booking_set").annotate(
            is_available=models.Case(
                models.When(
                    booking__check_in__lte=timezone.now(),
                    booking__check_out__gt=timezone.now(),
                    then=True,
                ),
                default=False,
                output_field=models.BooleanField(),
            )
        )


class Room(ModelsManager):
    room_number = models.IntegerField(unique=True)
    prise_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    phone_number = PhoneNumberField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review = GenericRelation(AbstractReview)

    objects = RoomQuerySet.as_manager()

    @property
    def is_available_status(self):
        if hasattr(self, "is_available"):
            return self.is_available
