from rest_framework import viewsets

from project_permissions.permissions import IsAdminOrReadOnly
from .models import Discount
from .serializers import DiscountModelSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountModelSerializer
    permission_classes = [IsAdminOrReadOnly]
