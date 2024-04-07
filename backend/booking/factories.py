import factory

from booking.models import Booking
from hotel_management.factories import UserFactory, RoomFactory


class BookingFactory(factory.Factory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    check_in = factory.Faker('date')
    check_out = factory.Faker('date')
    room = factory.SubFactory(RoomFactory)
    phone = factory.Faker('phone_number')
