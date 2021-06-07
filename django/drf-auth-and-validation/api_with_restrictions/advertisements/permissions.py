from rest_framework import permissions
from .models import Advertisement


class AdvertisementPermission(permissions.BasePermission):
    class Meta:
        model = Advertisement
        fields = '__all__'

    def has_permission(self, request, view, *args, **kwargs):
        self.message = 'Not allowed'
        self.pk = view.kwargs.get('pk')
        self.db_user = list(self.Meta.model.objects.filter(id=self.pk).select_related('creator'))[0].creator.username
        self.req_user = request.user.username
        if self.pk is None:
            self.message = 'Не задан ID'
            return False
        elif self.Meta.model.objects.filter(id=self.pk).count() != 1:
            self.message = 'Не верный id'
            return False
        elif self.db_user != self.req_user:
            self.message = 'Нельзя удалить объявление чужого пользователя'
            return False

        return True


