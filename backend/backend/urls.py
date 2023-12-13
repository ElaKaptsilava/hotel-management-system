"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from hotel_management.api import router as hotel_router
from booking.api import router as booking_router
from hotel_management.views import HotelReportApiView
from reviews.api import router as reviews_router
from discounts.api import router as discounts_router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Debug Toolbar
    path("__debug__/", include(debug_toolbar.urls)),
    # DRF spectacular views
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # Local views
    path(
        "hotel-management/",
        include((hotel_router.urls, "hotel-management"), namespace="hotel-management"),
    ),
    path(
        "bookings-management/",
        include(
            (booking_router.urls, "bookings-management"),
            namespace="bookings-management",
        ),
    ),
    path(
        "reviews-management/",
        include(
            (reviews_router.urls, "reviews-management"), namespace="reviews-management"
        ),
    ),
    path(
        "discounts-management/",
        include(
            (discounts_router.urls, "discounts-management"),
            namespace="discounts-management",
        ),
    ),
    # reports
    path("reports/", HotelReportApiView.as_view(), name="reports"),
    # JWT token views
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
