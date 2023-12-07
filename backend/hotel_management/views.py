from django_filters.rest_framework import DjangoFilterBackend
from project_permissions import permissions as project_permissions
from rest_framework import viewsets

from .filters import RoomFilters
from .models import Hotel, Location, Room
from .serializers import (
    HotelModelSerializer,
    LocationModelSerializer,
    RoomModelSerializer,
)


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer
    permission_classes = [project_permissions.IsAdminOrReadOnly]


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [project_permissions.IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilters


class LocationModelViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer
    permission_classes = [project_permissions.IsAdminOrReadOnly]
