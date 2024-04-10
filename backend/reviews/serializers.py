from rest_framework import serializers

from .models import AbstractReview


class AbstractReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractReview
        fields = "__all__"
