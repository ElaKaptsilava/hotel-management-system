from django.db import models

from hotel_management.models import Hotel, Room


class HotelReport(models.Model):
    hotel_name = models.CharField(max_length=256, default="hotel")
    avg_rate = models.FloatField()
    count_rooms = models.IntegerField()
    amount_of_occupied = models.IntegerField()
    hotel_occupancy_percentage = models.GeneratedField(
        expression=models.F("amount_of_occupied") * 100 / models.F("count_rooms"),
        output_field=models.FloatField(),
        db_persist=True,
    )

    generated = models.DateTimeField(auto_now=True)


class RoomReport(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount_of_booking = models.IntegerField(null=True, blank=True)
    avg_rate = models.FloatField(null=True, blank=True)
    next_arrival = models.DateField(null=True, blank=True)

    generated = models.DateTimeField(auto_now=True)
