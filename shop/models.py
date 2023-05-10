from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/static/shop/images/', default='shop/static/shop/images/default.png')
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + ' ' + str(self.count) + ' items'


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    cart_products = models.ManyToManyField(CartProduct)

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
        return self.user.username + ' ' + str(self.total_count) + ' items ' + str(self.total_price) + '$'
