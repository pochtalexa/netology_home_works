from rest_framework import permissions


class IsSelfAdvertisementPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        self.req_user = request.user.username
        self.obj_creator = obj.creator.username
        if self.req_user != self.obj_creator:
            self.message = 'Нельзя удалить объявление чужого пользователя'
            return False

        return True
