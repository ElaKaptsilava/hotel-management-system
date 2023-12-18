from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    HotelReportModelSerializer,
    RoomReportModelSerializer,
    BookingReportModelSerializer,
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
