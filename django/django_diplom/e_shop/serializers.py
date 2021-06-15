from rest_framework import serializers
from e_shop.models import Product, ProductReview, Order, ProductCollection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

    # def validate_mark(self, value):
    #     if value <= 0 or value >= 6:
    #         raise serializers.ValidationError("mark must be from 1 to 5")
    #     return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCollection
        fields = '__all__'




