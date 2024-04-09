import factory
from django.utils import timezone

from hotel_management.factories import RoomFactory
from .models import Discount


class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    pk = factory.Sequence(lambda n: n)
    value = factory.Faker("random_number", digits=3)
    percentage_value = factory.Faker("random_number", digits=2)
    generated = timezone.now()
    expiration_date = factory.Faker(
        "future_date", end_date="+30d", tzinfo=timezone.get_current_timezone()
    )

    @classmethod
    def rooms(cls, create, **kwargs):
        room = RoomFactory()
        discounts = super().rooms(create, **kwargs)
        discounts.toppings.add(room)
        return discounts
