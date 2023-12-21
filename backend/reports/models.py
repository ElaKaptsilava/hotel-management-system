from django.contrib.postgres.fields import ArrayField
from django.db import models

from hotel_management.models import Hotel, Room


class ReportAbstractModel(models.Model):
    hotel_name = models.CharField(max_length=256, default="hotel")
    generated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HotelReport(ReportAbstractModel):
    avg_rate = models.FloatField(null=True, blank=True)
    count_rooms = models.IntegerField()
    amount_of_occupied = models.IntegerField()
    count_discounts = models.PositiveIntegerField(default=0)
    hotel_occupancy_percentage = models.GeneratedField(
        expression=models.F("amount_of_occupied") * 100 / models.F("count_rooms"),
        output_field=models.FloatField(),
        db_persist=True,
    )


class BookingReport(ReportAbstractModel):
    count_booking = models.PositiveIntegerField()
    duration_avg = models.DurationField(null=True, blank=True)
    popular_countries = models.CharField(max_length=10, null=True)
    amount_of_occupied = models.IntegerField()


class RoomReport(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount_of_booking = models.IntegerField(null=True, blank=True)
    avg_rate = models.FloatField(null=True, blank=True)
    next_arrival = models.DateField(null=True, blank=True)

    generated = models.DateTimeField(auto_now=True)
