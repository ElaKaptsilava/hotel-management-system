"""This code generates a hotel report by calculating various statistics related to hotels and their rooms."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from hotel_management.models import Hotel, Room


@dataclass
class RoomReportRepr:
    """Data class represents a single room's report"""

    hotel: int
    room: int
    amount_of_booking: int
    avg_rate: float
    next_arrival: date


@dataclass
class HotelReportRepr:
    """Data class represents a single hotel's report"""

    hotel: str
    avg_rate: float
    count_rooms: int
    amount_of_occupied: int
    count_discounts: int


@dataclass
class BookingReport:
    """Data class represents a single booking's report"""

    hotel_name: str
    count_booking: int
    avg_duration: date
    popular_countries: str
    amount_of_occupied: int
