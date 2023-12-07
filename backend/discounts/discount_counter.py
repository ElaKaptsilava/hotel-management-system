"""
Implementation of discounts and promotions functionality
"""


class DiscountCounter:
    def is_percentage(self, valid_data) -> None:
        get_value, get_rooms = valid_data.get("value"), valid_data.get("rooms")
        if valid_data.get("is_percentage"):
            self.calculate_discount_if_percentage(value=get_value, rooms=get_rooms)
        for room in get_rooms:
            self.change_price_per_day_with_discount(discount=get_value, room=room)

    def calculate_discount_if_percentage(self, value: int, rooms) -> None:
        for room in rooms:
            calculate_discount = (room.prise_per_day * value) / 100
            self.change_price_per_day_with_discount(
                discount=calculate_discount, room=room
            )

    @staticmethod
    def change_price_per_day_with_discount(discount: float, room) -> None:
        room.prise_per_day -= discount
        room.save()
