from django_filters import rest_framework as filters
from .models import Product, ProductReview, Order, OrderPositions


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    description = filters.CharFilter(field_name="description", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('price', 'description', 'title')


class ProductReviewFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = ProductReview
        fields = ('id_author', 'id_product', 'created')


class OrderFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(field_name="created_at")
    updated = filters.DateFromToRangeFilter(field_name="updated_at")
    product = filters.CharFilter(field_name="positions__title", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ('status', 'sum', 'created', 'updated', 'product')



