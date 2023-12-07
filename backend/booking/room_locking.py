"""
Mechanism for blocking rooms during the reservation period.
"""


class RoomLocking:
    def is_available(self, valid_data) -> bool:
        room = valid_data.get("room")
        if room.status != "Available":
            is_available_dates = self.is_available_dates(
                room=room, valid_data=valid_data
            )
            if not is_available_dates:
                return False
        self.set_as_reserved(room=room)
        return True

    @staticmethod
    def is_available_dates(room, valid_data) -> bool:
        for booking in room.booking_set.all():
            if (
                valid_data.get("check_in") >= booking.check_in
                and valid_data.get("check_out") <= booking.check_out
            ):
                return False
        return True

    @staticmethod
    def set_as_reserved(room) -> None:
        room.status = "Reserved"
        room.save()
