from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import UserSerializer, AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsSelfAdvertisementPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    filter_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "destroy"]:
            return [IsAuthenticated(), IsSelfAdvertisementPermission()]
        elif self.action in ['retrieve', 'list']:
            return [AllowAny()]

        return []
