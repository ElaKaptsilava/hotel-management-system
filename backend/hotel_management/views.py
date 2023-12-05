from .models import Hotel, Location, Room
from .serializers import HotelModelSerializer, LocationModelSerializer, RoomModelSerializer

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class LocationModelViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer
    permission_classes = [IsAdminOrReadOnly]
