from rest_framework.routers import DefaultRouter

from .views import HotelReviewViewSet, RoomReviewViewSet

router = DefaultRouter()

router.register(r"hotels-reviews", HotelReviewViewSet, basename="hotels-reviews")
router.register(r"rooms-reviews", RoomReviewViewSet, basename="rooms-reviews")
