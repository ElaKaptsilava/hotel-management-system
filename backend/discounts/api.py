from rest_framework.routers import DefaultRouter

from .views import DiscountViewSet

router = DefaultRouter()

router.register(r"discounts", DiscountViewSet, basename="discounts")
