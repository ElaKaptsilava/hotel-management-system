import datetime
import random

import factory

from hotel_management.factories import RoomFactory, UserFactory

from .models import Booking


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    pk = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    check_in = factory.Faker("date_this_month")
    check_out = factory.LazyAttribute(
        lambda self: self.check_in + datetime.timedelta(days=random.randint(1, 31))
    )
    room = factory.SubFactory(RoomFactory)
