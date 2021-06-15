from django.contrib import admin
from .models import Product, ProductReview, Order, ProductCollection, OrderPositions


# TODO: добавить описание единственного и множественного числа


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderPositions)
class OrderPositionsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    pass


