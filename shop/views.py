from django.shortcuts import render, redirect

from .models import *
from .forms import *


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
    form = AddToCartForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AddToCartForm(request.POST)

            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get(user=request.user)

            if not cart.cart_products.filter(product=product).exists():
                cart_product = CartProduct.objects.create(product=product, count=int(form.data['count']))
                cart.cart_products.add(cart_product)
            else:
                cart_product = CartProduct.objects.get(product=product, cart=cart)
                cart_product.count += int(form.data['count'])

            cart_product.save()
        else:
            return redirect('login')


    data = {
        'product': product,
        'form': form,
    }

    return render(request, 'shop/product.html', data)
