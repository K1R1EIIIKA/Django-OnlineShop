from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/products/', default='static/images/default.png')
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    reviews = models.ManyToManyField('Review', blank=True)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return self.product.name + ' - ' + str(self.count) + ' items'


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    cart_products = models.ManyToManyField(CartProduct)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_price(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.product.price * cart_product.count
        return total

    is_bought = models.BooleanField(default=False)

    @property
    def total_count(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.count
        return total

    def __str__(self):
        return self.user.username + ' - ' + str(self.total_count) + ' items ' + str(self.total_price) + '$'


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.user.username + ' ' + str(self.date)


class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Без названия')
    text = models.CharField(max_length=255, default='Без текста')
    stars = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.user.username + ' - ' + str(self.title) + ' ' + str(self.stars) + ' stars'
