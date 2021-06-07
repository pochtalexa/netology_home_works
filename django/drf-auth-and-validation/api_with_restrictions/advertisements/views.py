from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import UserSerializer, AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import AdvertisementPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    filter_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        result = []
        if self.action in ["create", "update", "partial_update", "destroy"]:
            result.append(IsAuthenticated())
        if result and self.action == 'destroy':
            result.append(AdvertisementPermission())

        return result
