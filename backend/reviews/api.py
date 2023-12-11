from rest_framework.routers import DefaultRouter

from .views import AbstractReviewViewSet

app_name = "reviews-management"

router = DefaultRouter()

router.register(r"reviews", AbstractReviewViewSet, basename="hotels-reviews")
