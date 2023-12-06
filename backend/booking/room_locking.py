"""
Mechanism for blocking rooms during the reservation period.
"""


class RoomLocking:
    not_valid_status: list = ["NotAvailable", "Reserved", "Occupied"]

    def is_available(self, room) -> None or bool:
        if room.status in self.not_valid_status:
            return False
        self.set_as_reserved(room=room)

    @staticmethod
    def set_as_reserved(room) -> bool:
        room.status = "Reserved"
        room.save()
        return True
