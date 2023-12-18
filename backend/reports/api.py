from rest_framework.routers import DefaultRouter

from reports.views import HotelInitialModelViewSet

router = DefaultRouter()

router.register(
    r"hotel-reports-by-name", HotelInitialModelViewSet, basename="hotel-reports-by-name"
)
