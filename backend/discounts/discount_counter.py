"""
Implementation of discounts and promotions functionality
"""
from rest_framework import serializers


class DiscountCounter:
    """The `DiscountCounter` class provides methods for handling discounts and promotions related to room prices.

    Usage:
    - Call `is_percentage(valid_data)` when applying discounts to room prices.
    - Handle any raised `ValidationError` appropriately in your application logic."""

    @classmethod
    def is_percentage(cls, valid_data) -> None:
        get_value, get_rooms, get_percentage_value = (
            valid_data.get("value"),
            valid_data.get("rooms"),
            valid_data.get("percentage_value"),
        )
        for room in get_rooms:
            if get_percentage_value:
                cls.calculate_discount_if_percentage(
                    value=get_percentage_value, room=room
                )
            if get_value:
                cls.change_price_per_day_with_discount(discount=get_value, room=room)

    @classmethod
    def calculate_discount_if_percentage(cls, value: int, room) -> None:
        calculate_discount = (room.prise_per_day * value) / 100
        cls.change_price_per_day_with_discount(discount=calculate_discount, room=room)

    @classmethod
    def change_price_per_day_with_discount(cls, discount: float, room):
        room.prise_per_day -= discount
        if room.prise_per_day < 0:
            raise serializers.ValidationError("Price cannot be less than 0")
        room.save()
