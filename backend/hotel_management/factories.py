import factory
from django.contrib.auth.models import User

from .models import Hotel, Location, Room


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class LocationFactory(factory.Factory):
    class Meta:
        model = Location

    city = factory.Faker('city')
    country = factory.Faker('country')
    street = factory.Faker('street_name')
    state = factory.Faker('state')


class HotelFactory(factory.Factory):
    class Meta:
        model = Hotel

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    description = factory.Faker('paragraph')
    location = factory.SubFactory(LocationFactory)


class RoomFactory(factory.Factory):
    class Meta:
        model = Room

    room = factory.Sequence(lambda n: n)
    price_per_day = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    phone_number = factory.Faker('phone_number')
    hotel = factory.SubFactory(HotelFactory)
