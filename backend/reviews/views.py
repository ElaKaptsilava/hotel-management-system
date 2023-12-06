from .models import HotelReview, RoomReview
from .serializers import RoomReviewModelSerializer, HotelReviewModelSerializer

from rest_framework import viewsets


class RoomReviewViewSet(viewsets.ModelViewSet):
    queryset = RoomReview.objects.all()
    serializer_class = RoomReviewModelSerializer


class HotelReviewViewSet(viewsets.ModelViewSet):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewModelSerializer
