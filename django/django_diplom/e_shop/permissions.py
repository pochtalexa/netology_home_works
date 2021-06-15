from rest_framework import permissions


class IsMoreThanOneReview(permissions.BasePermission):
    def has_permission(self, request, view):
        self.req_user_id = request.user.id
        self.req_product_id = request.data.get('id_product')
        # self.review_qnty = self.Meta.model.objects.filter(id_author=self.req_user_id, id_product=self.req_product_id).count()
        self.review_qnty = view.queryset.filter(id_author=self.req_user_id, id_product=self.req_product_id).count()

        if self.review_qnty >= 1:
            self.message = "Нельзя создавать более одного отзыва на товар"
            return False

        return True


class IsSelfReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        self.req_user_id = request.user.id
        self.obj_author_id = obj.id_author_id

        if self.req_user_id != self.obj_author_id:
            self.message = 'Нельзя удалять или редактировать объявление другого пользователя'
            return False

        return True


class IsSelfOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        self.req_user_id = request.user.id
        self.obj_user_id = obj.id_user_id

        if self.req_user_id != self.obj_user_id:
            self.message = 'Нельзя удалить или посмотреть чужой заказ'
            return False

        return True


class DenyAny(permissions.BasePermission):
    def has_permission(self, request, view):
        self.message = 'Метод не определен'
        return False

    def has_object_permission(self, request, view, obj):
        self.message = 'Метод не определен'
        return False
