from rest_framework.routers import DefaultRouter

from .views import BookingModelViewSet

router = DefaultRouter()
app_name = "booking-management"


router.register(r"bookings", BookingModelViewSet, basename="bookings")
