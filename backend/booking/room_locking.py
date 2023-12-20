"""
Mechanism for blocking rooms during the reservation period.
"""
from django.db import models
from rest_framework.exceptions import APIException


class RoomLocking:
    """`RoomLocking`, provides methods to check room availability and prevent double booking during the reservation process.

    Usage:
    - Call `is_available(valid_data)` before confirming a reservation to ensure the room is available.
    - Handle the raised `APIException` appropriately in your application logic."""

    @classmethod
    def is_available(cls, valid_data) -> bool:
        room = valid_data.get("room")
        if room.is_available_status:
            cls.is_available_dates(room=room, valid_data=valid_data)
        return True

    @classmethod
    def is_available_dates(cls, room, valid_data) -> bool:
        is_available = room.booking_set.filter(
            models.Q(
                check_in__lte=valid_data.get("check_in"),
                check_out__gt=valid_data.get("check_in"),
            )
            or models.Q(
                check_in__lt=valid_data.get("check_out"),
                check_out__gte=valid_data.get("check_out"),
            )
        ).exists()
        if is_available:
            raise APIException(
                f"This room is occupied from {valid_data.get('check_in')} to {valid_data.get('check_out')}."
                f"You should choose another date"
            )
        return True
