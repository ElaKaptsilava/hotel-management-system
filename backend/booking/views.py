from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingModelSerializer
from hotel_management import models as hotel_models


class CreateBookingModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room = hotel_models.Room.objects.get(pk=instance.room.pk)
        room.status = 'Available'
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
