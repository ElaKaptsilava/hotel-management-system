from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

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
    phone = PhoneNumberField(null=True, blank=True)
    duration = models.GeneratedField(
        expression=models.F("check_out") - models.F("check_in"),
        output_field=models.DurationField(),
        db_persist=True,
        null=True,
        blank=True,
    )

    objects = BookingQuerySet.as_manager()

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(user={self.user.name!r}, room={self.room!r})"

    @property
    def is_active_status(self) -> bool:
        if hasattr(self, "is_active"):
            return self.is_active
        return True if self.check_in == timezone.now().date() else False
