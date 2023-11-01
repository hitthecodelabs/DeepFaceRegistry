from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.permissions.api.serializers import PermissionSerializer


class PermissionsViewSet(ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = serializer_class.Meta().model.objects.all()
    response = None
