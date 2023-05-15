from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_all, name='products'),
    path('products/<int:product_id>', views.product_info, name='product'),
]
