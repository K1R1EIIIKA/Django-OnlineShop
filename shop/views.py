from django.shortcuts import render

from .models import *


def home(request):
    carts = Cart.objects.all()

    data = {
        'carts': carts,
    }
    return render(request, 'shop/home.html', data)
