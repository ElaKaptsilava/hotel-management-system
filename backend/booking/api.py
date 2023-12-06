from rest_framework.routers import DefaultRouter

from .views import CreateBookingModelViewSet, BookingModelViewSet

router = DefaultRouter()


router.register(r'bookings-users', CreateBookingModelViewSet, basename='bookings-users')
router.register(r'bookings-admin', BookingModelViewSet, basename='bookings-admin')
