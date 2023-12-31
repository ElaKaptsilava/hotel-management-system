from rest_framework.routers import DefaultRouter

from reports.views import HotelReportApiView, RoomReportApiView

router = DefaultRouter()

app_name = "reports"

router.register(r"hotels", HotelReportApiView, basename="hotels")
router.register(r"rooms", RoomReportApiView, basename="rooms")
# router.register(
#     r"booking-reports", BookingReportInitialModelViewSet, basename="booking-reports"
# )

# /reports/report-room/id:hotel/
