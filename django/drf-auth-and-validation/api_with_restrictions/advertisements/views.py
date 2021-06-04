from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework import serializers, status
from .models import Advertisement
from .serializers import UserSerializer, AdvertisementSerializer


class AdvertisementFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="creator__username", lookup_expr='iexact')
    created = filters.DateFromToRangeFilter(field_name="created_at")
    updated = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Advertisement
        fields = '__all__'


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    class Meta:
        model = Advertisement
        # fields = ('id', 'title', 'description', 'creator',
        #           'status', 'created_at', )
        fields = '__all__'

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    filter_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    def destroy(self, request, pk=None):
        # self.db_user_qnty = self.Meta.model.objects.filter(id=pk).count()
        self.db_user = list(self.Meta.model.objects.filter(id=pk).select_related('creator'))[0].creator.username
        self.req_user = self.request.user.username
        if pk is None:
            raise serializers.ValidationError('Не задан ID')
        elif self.Meta.model.objects.filter(id=pk).count() != 1:
            raise serializers.ValidationError('Не верный id')
        elif self.db_user != self.req_user:
            raise serializers.ValidationError('Нельзя удалить объявление чужого пользователя')
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
