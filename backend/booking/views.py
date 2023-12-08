from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from .models import Booking
from .serializers import BookingModelSerializer
from hotel_management import models as hotel_models
from project_permissions.permissions import CustomPermission


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [CustomPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room = hotel_models.Room.objects.get(pk=instance.room.pk)
        room.status = "Available"
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
