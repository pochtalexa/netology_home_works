from django.conf import settings
from django.core import validators
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductReview(models.Model):
    id_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ID автора отзыва')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='ID товара')
    review = models.TextField(verbose_name='Текст отзыва')

    # TODO: поле нужно будет проверить в сериалайзере - проверить реализацию
    mark = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderStatusChoices(models.TextChoices):
    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS ", "В работе"
    DONE = "DONE", "Закрыт"


class OrderPositions(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='ID товара')
    id_order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='ID заказа')
    quantity = models.IntegerField(verbose_name='количество единиц товара')


class Order(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ID пользователя')
    positions = models.ManyToManyField(Product, through=OrderPositions)
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW
    )
    sum = models.FloatField(verbose_name='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductCollection(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    selection = models.ManyToManyField(Product, verbose_name='элементы подборки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
