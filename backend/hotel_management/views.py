from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from project_permissions.permissions import IsAdminOrReadOnly
from rest_framework import viewsets

from .filters import RoomFilters
from .models import Hotel, Location, Room
from .reports import HotelReportGenerate
from .serializers import (
    HotelModelSerializer,
    LocationModelSerializer,
    RoomModelSerializer,
    HotelReportModelSerializer,
)


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


class HotelReportApiView(APIView):
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get(self, request):
        data = HotelReportGenerate.hotel_report()
        serializer = HotelReportModelSerializer(instance=data, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
