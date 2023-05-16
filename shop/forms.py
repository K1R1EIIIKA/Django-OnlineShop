from django.forms import TextInput, EmailInput, CharField, PasswordInput, ModelForm, ImageField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from .models import CartProduct


class AddToCartForm(ModelForm):
    class Meta:
        model = CartProduct
        fields = ['count']

        widgets = {
            'count': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество',
                'type': 'number',
                'min': '1',
                'max': '100',
            }),
        }
