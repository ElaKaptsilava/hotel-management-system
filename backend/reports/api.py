from rest_framework.routers import DefaultRouter

from reports.views import (
    HotelInitialModelViewSet,
    RoomInitialModelViewSet,
    BookingReportInitialModelViewSet,
)

router = DefaultRouter()

app_name = "reports"

router.register(r"hotel-reports", HotelInitialModelViewSet, basename="hotel-reports")
router.register(r"room-reports", RoomInitialModelViewSet, basename="room-reports")
router.register(
    r"booking-reports", BookingReportInitialModelViewSet, basename="booking-reports"
)
