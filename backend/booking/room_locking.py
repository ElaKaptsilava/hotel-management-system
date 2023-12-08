"""
Mechanism for blocking rooms during the reservation period.
"""
from hotel_management.models import Room


class RoomLocking:
    @classmethod
    def is_available(cls, valid_data) -> bool:
        room = valid_data.get("room")
        if room.status != Room.Status.available:
            is_available_dates = cls.is_available_dates(
                room=room, valid_data=valid_data
            )
            if not is_available_dates:
                return False
        cls.set_as_reserved(room=room)
        return True

    @classmethod
    def is_available_dates(cls, room, valid_data) -> bool:
        for booking in room.booking_set.all():
            if (
                booking.check_in <= valid_data.get("check_in") <= booking.check_out
                or booking.check_in <= valid_data.get("check_out") <= booking.check_out
            ):
                return False
        return True

    @classmethod
    def set_as_reserved(cls, room) -> None:
        room.status = Room.Status.reserved
        room.save()
