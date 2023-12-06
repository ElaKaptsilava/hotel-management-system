from .models import HotelReview, RoomReview
from .serializers import RoomReviewModelSerializer, HotelReviewModelSerializer

from rest_framework import viewsets, permissions
from project_permissions import permissions as project_permissions


class RoomReviewViewSet(viewsets.ModelViewSet):
    queryset = RoomReview.objects.all()
    serializer_class = RoomReviewModelSerializer
    permission_classes = (project_permissions.CustomPermission,)


class HotelReviewViewSet(viewsets.ModelViewSet):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewModelSerializer
    permission_classes = (project_permissions.CustomPermission,)
