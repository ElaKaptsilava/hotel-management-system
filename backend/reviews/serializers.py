from .models import AbstractReview

from rest_framework import serializers


class AbstractReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractReview
        fields = "__all__"
