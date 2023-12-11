from .models import AbstractReview
from .serializers import AbstractReviewModelSerializer

from rest_framework import viewsets, permissions
from project_permissions import permissions as project_permissions


class AbstractReviewViewSet(viewsets.ModelViewSet):
    queryset = AbstractReview.objects.all()
    serializer_class = AbstractReviewModelSerializer
    permission_classes = (project_permissions.CustomPermission,)
