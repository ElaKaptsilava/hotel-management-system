from django.contrib import admin
from .models import HotelReport, RoomReport


@admin.register(HotelReport)
class HotelReportAdmin(admin.ModelAdmin):
    list_display = ("hotel_name", "count_rooms", "amount_of_occupied")


@admin.register(RoomReport)
class RoomReportAdmin(admin.ModelAdmin):
    list_display = ("hotel", "room", "next_arrival")
