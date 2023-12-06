from .models import RoomReview, HotelReview

from rest_framework import serializers


class RoomReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReview
        fields = "__all__"


class HotelReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = "__all__"
