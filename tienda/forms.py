from turtle import textinput
from django import forms
from django.core import validators

from django.contrib.auth.forms import UserCreationForm
from tienda.models import Article
from tienda.models import Prueba
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
class CartForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titlecart', 'contentcart',]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'user', 'categories',]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',]

class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['title', 'content', 'image', 'user', 'categories',]
