from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingModelSerializer
from hotel_management import models as hotel_models
from project_permissions.permissions import PermissionHandler
from django.db import transaction


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.with_booking()
    serializer_class = BookingModelSerializer
    permission_classes = [PermissionHandler]

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room = hotel_models.Room.objects.get(pk=instance.room.pk)
        room.status = "Available"
        room.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
