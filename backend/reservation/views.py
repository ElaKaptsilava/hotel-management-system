from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins

from .models import Booking
from .serializers import BookingModelSerializer
from hotel_management import permissions as hotel_permissions


class CreateBookingModelViewSet(mixins.CreateModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [hotel_permissions.IsAdminOrReadOnly]
