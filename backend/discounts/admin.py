from django.contrib import admin

from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("value", "percentage_value", "generated")
    list_filter = ("value", "percentage_value", "generated")
    sortable_by = "generated"
    ordering = ("generated",)
