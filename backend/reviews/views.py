from project_permissions.permissions import PermissionHandler
from rest_framework import viewsets

from .models import AbstractReview
from .serializers import AbstractReviewModelSerializer


class AbstractReviewViewSet(viewsets.ModelViewSet):
    queryset = AbstractReview.objects.all()
    serializer_class = AbstractReviewModelSerializer
    permission_classes = [PermissionHandler]
