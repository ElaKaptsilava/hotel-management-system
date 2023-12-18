from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from hotel_management import models as hotel_models


class BookingQuerySet(QuerySet):
    def with_booking(self):
        return self.annotate(
            is_active=models.Case(
                models.When(
                    check_in__lte=timezone.now(),
                    check_out__gt=timezone.now(),
                    then=True,
                ),
                default=False,
                output_field=models.BooleanField(),
            )
        )


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField(default=timezone.now)
    room = models.ForeignKey(hotel_models.Room, on_delete=models.CASCADE, null=True)

    objects = BookingQuerySet.as_manager()

    @property
    def is_active_status(self):
        if hasattr(self, "is_active"):
            return self.is_active
