from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "check_in", "check_out", "is_active_status")
    list_filter = ("check_in", "check_out")
