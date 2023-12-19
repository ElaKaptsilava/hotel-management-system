from rest_framework.routers import DefaultRouter

from reports.views import HotelInitialModelViewSet, RoomInitialModelViewSet

router = DefaultRouter()

router.register(r"hotel-reports", HotelInitialModelViewSet, basename="hotel-reports")
router.register(r"room-reports", RoomInitialModelViewSet, basename="room-reports")
