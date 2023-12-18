from django.urls import path
from rest_framework.routers import DefaultRouter

from reports.views import HotelReportApiView, RoomReportApiView, BookingReportApiView

urlpatterns = [
    path("hotel-reports/", HotelReportApiView.as_view(), name="hotel-reports"),
    path("room-reports/", RoomReportApiView.as_view(), name="room-reports"),
    path("booking-reports/", BookingReportApiView.as_view(), name="booking-reports"),
]
