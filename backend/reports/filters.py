import django_filters
from hotel_management.models import Hotel


class HotelFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="incontains")

    class Meta:
        model = Hotel
        fields = ["name"]
