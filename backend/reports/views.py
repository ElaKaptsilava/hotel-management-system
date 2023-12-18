from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from hotel_management.models import Hotel
from .serializers import (
    HotelReportModelSerializer,
    RoomReportModelSerializer,
    BookingReportModelSerializer,
    HotelInitialModelSerializer,
)
from .reports_generation import (
    HotelReportGenerate,
    RoomReportGenerate,
    BookingReportGenerate,
)


class HotelReportApiView(APIView):
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get(self, request):
        data = HotelReportGenerate.hotel_report()
        serializer = HotelReportModelSerializer(instance=data, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RoomReportApiView(APIView):
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get(self, request):
        data = RoomReportGenerate.room_report()
        serializer = RoomReportModelSerializer(instance=data, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BookingReportApiView(APIView):
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get(self, request):
        data = BookingReportGenerate.booking_report()
        serializer = BookingReportModelSerializer(instance=data, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class HotelInitialModelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelInitialModelSerializer
    queryset = Hotel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer_initial_hotel = self.serializer_class(data=request.data)
        serializer_initial_hotel.is_valid(raise_exception=True)
        hotel_name = serializer_initial_hotel.validated_data.get("name", None)
        report = HotelReportGenerate.hotel_report(hotel_name)
        serializer_hotel = HotelReportModelSerializer(data=report, many=True)
        serializer_hotel.is_valid()
        serializer_hotel.save()
        return Response(serializer_hotel.data, status=status.HTTP_201_CREATED)
