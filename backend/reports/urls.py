from django.contrib import admin
from django.urls import path

from reports.views import HotelReportApiView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hotel_reports/", HotelReportApiView.as_view(), name="hotel-reports"),
]
