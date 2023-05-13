from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_home, name='account_home'),
    path('settings', views.settings, name='settings'),
    path('register', views.register, name='register'),
    path('login', views.login_acc, name='login'),
    path('logout', views.logout_acc, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
