from .models import Discount

from rest_framework import serializers


class DiscountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"
