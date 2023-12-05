from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Booking
from .serializers import BookingModelSerializer


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    filter_backends = [DjangoFilterBackend]