"""
Implementation of discounts and promotions functionality
"""
from rest_framework import serializers


class DiscountCounter:
    @classmethod
    def is_percentage(cls, valid_data) -> None:
        get_value, get_rooms = valid_data.get("value"), valid_data.get("rooms")
        for room in get_rooms:
            if valid_data.get("is_percentage"):
                cls.calculate_discount_if_percentage(value=get_value, room=get_rooms)
            else:
                cls.change_price_per_day_with_discount(discount=get_value, room=room)

    @classmethod
    def calculate_discount_if_percentage(cls, value: int, room) -> None:
        calculate_discount = (room.prise_per_day * value) / 100
        cls.change_price_per_day_with_discount(discount=calculate_discount, room=room)

    @classmethod
    def change_price_per_day_with_discount(cls, discount: float, room) -> None:
        room.prise_per_day -= discount
        if room.prise_per_day < 0:
            raise serializers.ValidationError("Price cannot be less than 0")
        else:
            room.save()
