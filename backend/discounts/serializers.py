from django.db import transaction
from rest_framework import serializers

from hotel_management.models import Room

from .discount_counter import DiscountCounter
from .models import Discount


class DiscountModelSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())

    class Meta:
        model = Discount
        fields = ["id", "value", "percentage_value", "rooms"]

    @transaction.atomic
    def create(self, validated_data: dict) -> Discount:
        DiscountCounter.is_percentage(valid_data=validated_data)
        create_discount = Discount.objects.create(
            value=validated_data.get("value"),
            percentage_value=validated_data.get("percentage_value"),
        )
        create_discount.rooms.set(validated_data.get("rooms"))
        return create_discount
