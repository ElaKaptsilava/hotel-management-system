from django.contrib import admin

from .models import AbstractReview


@admin.register(AbstractReview)
class AbstractReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rate", "title", "content_object")
