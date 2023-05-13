from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import *
from .forms import *


@login_required(login_url='login')
def account_home(request):
    user_info = UserInfo.objects.get(user=request.user)

    data = {
        'user_info': user_info,
    }

    return render(request, 'account/account_home.html', data)


@login_required(login_url='login')
def settings(request):
    error = ''

    user_info = UserInfo.objects.get(user=request.user)
    form = UserInfoForm(instance=user_info)

    if request.method == 'POST':
        form = UserInfoForm(request.POST, request.FILES, instance=user_info)

        if form.is_valid():
            if form.cleaned_data['email'] in UserInfo.objects.all().values_list('email', flat=True) and \
                    UserInfo.objects.get(email=form.cleaned_data['email']).user != request.user:
                error = 'Пользователь с таким email уже существует'

                return render(request, 'account/settings.html', {'form': form, 'error': error})

            if form.cleaned_data['phone'] in UserInfo.objects.all().values_list('phone', flat=True) and \
                    UserInfo.objects.get(phone=form.cleaned_data['phone']).user != request.user:
                error = 'Пользователь с таким номером телефона уже существует'

                return render(request, 'account/settings.html', {'form': form, 'error': error})

            form.save()
        else:
            error = 'Неправильно введенные данные'

    data = {
        'form': form,
        'user_info': user_info,
        'error': error,
    }

    return render(request, 'account/settings.html', data)


def register(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()

                UserInfo.objects.create(
                    user=User.objects.get(username=form.cleaned_data['username']),
                    email=form.cleaned_data['email'])

                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)

                login(request, user)
                return redirect('account_home')
            else:
                error = 'Неправильно введенные данные'

        data = {
            'form': form,
            'error': error
        }

        return render(request, 'registration/register.html', data)


def login_acc(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = Authenticate()

        if request.method == 'POST':
            form = Authenticate(data=request.POST)

            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')

                if not UserInfo.objects.filter(user=User.objects.get(username=username)).exists():
                    UserInfo.objects.create(
                        user=User.objects.get(username=username),
                        email=User.objects.get(username=username).email)

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('account_home')
            else:
                error = 'Неправильно введенные данные'
        data = {
            'form': form,
            'error': error,
        }

    return render(request, 'registration/login.html', data)


@login_required(login_url='login')
def logout_acc(request):
    if request.user.is_authenticated:
        logout(request)

        return redirect('home')
