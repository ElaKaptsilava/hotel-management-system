from rest_framework.routers import DefaultRouter

from .views import BookingModelViewSet

router = DefaultRouter()


router.register(r"bookings", BookingModelViewSet, basename="bookings")
