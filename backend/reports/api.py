from reports.views import HotelReportApiView, RoomReportApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = "reports"

router.register(r"hotels", HotelReportApiView, basename="hotels")
router.register(r"rooms", RoomReportApiView, basename="rooms")
