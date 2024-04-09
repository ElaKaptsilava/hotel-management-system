from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hotel_management.models import Hotel, Room
from hotel_management.serializers import HotelModelSerializer
from .booking_reports import BookingReportGenerate
from .hotel_reports import HotelReportGenerate
from .room_reports import RoomReportGenerate, RoomsGenerate
from .serializers import (
    HotelReportSerializer,
    RoomInitialModelSerializer,
    RoomReportSerializer,
    RoomsPageReportSerializer,
)
from .paginations import RoomResultsSetPagination
from .filters import HotelFilters


class HotelReportApiView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilters

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

    @action(methods=["GET"], detail=True, url_name="get-rooms")
    def get_rooms(self, request, pk):
        instance_hotel = self.get_object()
        rooms = Room.objects.filter(hotel=instance_hotel)
        serializer = RoomInitialModelSerializer(instance=rooms, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomReportApiView(mixins.ListModelMixin, GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomInitialModelSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]
    pagination_class = RoomResultsSetPagination

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        room_instance = self.get_object()
        room_report = RoomReportGenerate.generate_room_report(
            room_instance=room_instance
        )
        serializer = RoomReportSerializer(data=room_report.__dict__)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, url_name="page-reports")
    def get_page_room_reports(self, request):
        rooms_instance = self.paginate_queryset(self.get_queryset().order_by('room_number'))
        rooms_queryset = Room.objects.filter(
            id__in=[room.id for room in rooms_instance]
        )
        room_report = RoomsGenerate.generate_rooms_report(rooms=rooms_queryset)
        serializer = RoomsPageReportSerializer(data=room_report.__dict__)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
