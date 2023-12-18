"""This code generates a hotel report by calculating various statistics related to hotels and their rooms."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from hotel_management.models import Hotel, Room


@dataclass
class RoomReport:
    """Data class represents a single room's report"""

    hotel_name: str
    room_number: int
    amount_of_booking: int
    avg_rate: Decimal
    next_arrival: date


@dataclass
class HotelReport:
    """Data class represents a single hotel's report"""

    hotel: Hotel
    avg_rate: Decimal
    count_rooms: int
    amount_of_reserved: int
    amount_of_available: int
    hotel_occupancy_percentage: int


@dataclass
class BookingReport:
    """Data class represents a single booking's report"""

    hotel: Hotel
    room: Room
    arrival: date
    check_out: date
