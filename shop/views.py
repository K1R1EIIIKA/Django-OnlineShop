from django.shortcuts import render

from .models import *


def home(request):
    top_products = Product.objects.all()[:8]

    data = {
        'top_products': top_products,
    }

    return render(request, 'shop/home.html', data)


def products_all(request):
    products = Product.objects.all()

    data = {
        'products': products,
    }

    return render(request, 'shop/products.html', data)


def product_info(request, product_id):
    product = Product.objects.get(id=product_id)

    data = {
        'product': product,
    }

    return render(request, 'shop/product.html', data)
