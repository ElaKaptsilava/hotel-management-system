import django_filters
from .models import Room


class RoomFilters(django_filters.FilterSet):
    hotel = django_filters.CharFilter(
        field_name="hotel__name", lookup_expr="incontains"
    )
    location = django_filters.CharFilter(
        field_name="hotel__location__city", lookup_expr="incontains"
    )
    price = django_filters.NumericRangeFilter(
        field_name="prise_per_day", lookup_expr="range"
    )
    status = django_filters.ChoiceFilter(
        choices=Room.Status.choices, field_name="status", lookup_expr="contains"
    )

    class Meta:
        model = Room
        fields = ["hotel", "prise_per_day", "status"]
