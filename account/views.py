from django.shortcuts import render

from .models import *


def account_home(request):
    user_info = UserInfo.objects.get(user=request.user)

    data = {
        'user_info': user_info,
    }

    return render(request, 'account/account_home.html', data)
