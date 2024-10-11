from django import forms
from django.core import validators

from django.contrib.auth.forms import UserCreationForm
from tienda.models import Article, VendedorConfiguracion, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'user', 'categories',]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',]


class VendedorConfiguracionForm(forms.ModelForm):
    class Meta:
        model = VendedorConfiguracion
        fields = ['telefono', 'tiendafisica_tf', 'direccion', 'horario_atencion', 'envio', ]

class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['paypal_account', 'whatsapp_account', 'mail_account']

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Asunto')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
    email = forms.EmailField(label='Tu correo')