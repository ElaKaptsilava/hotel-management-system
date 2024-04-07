import factory

from .models import Booking
from hotel_management.factories import UserFactory, RoomFactory


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    pk = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    check_in = factory.Faker('date')
    check_out = factory.Faker('date')
    room = factory.SubFactory(RoomFactory)
    phone = factory.Faker('phone_number')
