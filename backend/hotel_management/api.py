from rest_framework.routers import DefaultRouter

from hotel_management import views as hotel_views
from reservation import views as booking_views

from .views import HotelModelViewSet, LocationModelViewSet, RoomModelViewSet

router = DefaultRouter()

router.register(r'hotels', HotelModelViewSet, basename='hotels')
router.register(r'locations', LocationModelViewSet, basename='locations')
router.register(r'rooms', RoomModelViewSet, basename='rooms')
