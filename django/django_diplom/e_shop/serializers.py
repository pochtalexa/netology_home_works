from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from e_shop.models import Product, ProductReview, Order, ProductCollection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ProductReview.objects.all(),
                fields=['author', 'product']
            )
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCollection
        fields = '__all__'
