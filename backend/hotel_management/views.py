from .models import Hotel, Location, Room
from .serializers import HotelModelSerializer, LocationModelSerializer, RoomModelSerializer

from rest_framework import viewsets


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer


class LocationModelViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer
