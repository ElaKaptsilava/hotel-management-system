from django.db import transaction
from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hotel_management.models import Hotel, Room
from hotel_management.serializers import HotelModelSerializer, RoomModelSerializer
from .booking_reports import BookingReportGenerate
from .hotel_reports import HotelReportGenerate
from .room_reports import RoomReportGenerate
from .serializers import (
    HotelReportSerializer,
    RoomInitialModelSerializer,
)


class HotelReportApiView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    @action(methods=["GET"], detail=True, url_name="hotel-reports")
    def get_hotel_reports(self, request, pk):
        instance_hotel = self.get_object()
        hotel_report = HotelReportGenerate.generate_hotel_report(
            instance_hotel=instance_hotel
        )
        serializer = HotelReportSerializer(data=hotel_report.__dict__)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True, url_name="booking-reports")
    def get_booking_reports(self, request, pk):
        instance_hotel = self.get_object()
        booking_report = BookingReportGenerate.generate_booking_report(instance_hotel)
        serializer = HotelReportSerializer(data=booking_report.__dict__)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)


class RoomReportApiView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Room.objects.all()
    serializer_class = RoomInitialModelSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        room_instance = self.get_object()
        room_report = RoomReportGenerate.generate_room_report(
            room_instance=room_instance
        )
        serializer = HotelReportSerializer(data=room_report.__dict__)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)


#
# class BookingReportApiView(APIView):
#     permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]
#
#     def get(self, request):
#         data = BookingReportGenerate.booking_report()
#         serializer = BookingReportModelSerializer(instance=data, many=True)
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
