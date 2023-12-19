from django.db import transaction, models
from django.utils import timezone
from rest_framework import permissions, status, mixins
from rest_framework.response import Response
from rest_framework import viewsets

from .models import HotelReport, RoomReport
from .serializers import (
    RoomReportModelSerializer,
    HotelInitialModelSerializer,
    HotelReportModelSerializer,
    RoomReportInitialModelSerializer,
)
from .reports_generation import (
    HotelReportGenerate,
    RoomReportGenerate,
)


class RoomInitialModelViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = RoomReportInitialModelSerializer
    queryset = RoomReport.objects.filter(
        models.Q(generated__month=timezone.now().month)
    )
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer_initial_room = self.serializer_class(data=request.data)
        serializer_initial_room.is_valid(raise_exception=True)
        hotel = serializer_initial_room.validated_data.get("hotel", None)
        reports = RoomReportGenerate.room_report(hotel)
        serializer_room = RoomReportInitialModelSerializer(data=reports, many=True)
        serializer_room.is_valid(raise_exception=True)
        serializer_room.save()
        return Response(serializer_room.validated_data, status=status.HTTP_201_CREATED)


class HotelInitialModelViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = HotelInitialModelSerializer
    queryset = HotelReport.objects.filter(
        models.Q(generated__month=timezone.now().month)
    )
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer_initial_hotel = self.serializer_class(data=request.data)
        serializer_initial_hotel.is_valid(raise_exception=True)
        hotel_name = serializer_initial_hotel.validated_data.get("hotel_name", None)
        report = HotelReportGenerate.hotel_report(hotel_name)
        serializer_hotel = HotelReportModelSerializer(data=report.__dict__)
        serializer_hotel.is_valid(raise_exception=True)
        serializer_hotel.save()
        return Response(serializer_hotel.validated_data, status=status.HTTP_201_CREATED)
