from .models import AbstractReview
from .serializers import AbstractReviewModelSerializer

from rest_framework import viewsets
from project_permissions.permissions import PermissionHandler


class AbstractReviewViewSet(viewsets.ModelViewSet):
    queryset = AbstractReview.objects.all()
    serializer_class = AbstractReviewModelSerializer
    permission_classes = [PermissionHandler]
