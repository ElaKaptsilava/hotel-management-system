from rest_framework.routers import DefaultRouter

from hotel_management import views as hotel_views
from reservation import views as booking_views

router = DefaultRouter()

router.register(r'hotels', hotel_views.HotelModelViewSet, basename='hotels')
router.register(r'locations', hotel_views.LocationModelViewSet, basename='locations')
router.register(r'rooms', hotel_views.RoomModelViewSet, basename='rooms')

router.register(r'bookings', booking_views.BookingModelViewSet, basename='bookings')