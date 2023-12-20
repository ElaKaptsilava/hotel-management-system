from rest_framework.routers import DefaultRouter

from .views import DiscountViewSet

app_name = "discounts-management"

router = DefaultRouter()

router.register(r"discounts", DiscountViewSet, basename="discounts")
