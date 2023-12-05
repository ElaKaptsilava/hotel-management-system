from django_filters.rest_framework import DjangoFilterBackend

from .models import Hotel, Location, Room
from .serializers import HotelModelSerializer, LocationModelSerializer, RoomModelSerializer
from .filters import RoomFilters
from .permissions import IsAdminOrReadOnly

from rest_framework import viewsets


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilters


class LocationModelViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer
    permission_classes = [IsAdminOrReadOnly]
