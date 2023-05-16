from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(blank=True, default='static/images/default.png', verbose_name='Изображение')
    description = models.CharField(max_length=255, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    reviews = models.ManyToManyField('Review', blank=True, verbose_name='Отзывы')

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def average_stars(self):
        total = 0
        for review in self.reviews.all():
            total += review.stars

        if self.review_count > 0:
            return total / self.review_count
        else:
            return 0

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name + ' ' + str(self.price) + '$' + ' - ' + str(self.review_count) + ' reviews'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.IntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return self.product.name + ' - ' + str(self.count) + ' items'


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    cart_products = models.ManyToManyField(CartProduct, blank=True, verbose_name='Товары в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_price(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.product.price * cart_product.count
        return total

    is_bought = models.BooleanField(default=False, verbose_name='Куплена')

    @property
    def total_count(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.count
        return total

    def __str__(self):
        return self.user.username + ' - ' + str(self.total_count) + ' items ' + str(self.total_price) + '$'


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.user.username + ' ' + str(self.date)


class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=100, default='Без названия', verbose_name='Название')
    text = models.CharField(max_length=255, default='Без текста', verbose_name='Текст')
    stars = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                             verbose_name='Количество звезд')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.user.username + ' - ' + str(self.title) + ' ' + str(self.stars) + '*'
