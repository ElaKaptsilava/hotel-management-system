import factory
from django.contrib.auth.models import User
from phonenumber_field.phonenumber import to_python

from .models import Hotel, Location, Room
import faker

fake = faker.Faker()


def generate_phone_number():
    fake_phone_number = fake.phone_number()
    phone_number_obj = to_python(fake_phone_number, region="US")
    if phone_number_obj.is_valid():
        return str(phone_number_obj)
    else:
        return generate_phone_number()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    pk = factory.Sequence(lambda n: n)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    pk = factory.Sequence(lambda n: n)
    city = factory.Faker("city")
    country = factory.Faker("country")
    street = factory.Faker("street_name")
    state = factory.Faker("state")


class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    pk = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    description = factory.Faker("paragraph")
    location = factory.SubFactory(LocationFactory)


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    pk = factory.Sequence(lambda n: n)
    room_number = factory.Sequence(lambda n: n)
    prise_per_day = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    phone_number = factory.LazyFunction(generate_phone_number)
    hotel = factory.SubFactory(HotelFactory)
