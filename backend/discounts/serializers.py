from django.db import transaction

from .models import Discount

from rest_framework import serializers
from .discount_counter import DiscountCounter


class DiscountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data: dict) -> Discount:
        DiscountCounter.is_percentage(valid_data=validated_data)
        create_discount = Discount.objects.create(
            value=validated_data.get("value"),
            percentage_value=validated_data.get("percentage_value"),
        )
        create_discount.rooms.set(validated_data.get("rooms"))
        return create_discount
