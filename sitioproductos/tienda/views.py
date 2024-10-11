from django.shortcuts import render
from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from tienda import forms
from tienda.forms import ProductForm
from tienda.forms import PruebaForm, CartForm
from tienda.models import Category, Article
from django.core.paginator import Paginator
#mainapp
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from tienda.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import User

# Create your views here

def list(request):

    articles = Article.objects.all()
    
    # Paginar Articulos
    paginator = Paginator(articles, 100)
    

    # Recoger numero pagina
    page = request.GET.get('page')
    page_articles = paginator.get_page(page)

    cartform = CartForm()


    if request.method == 'POST':
        cartform = CartForm(request.POST)
        
        if cartform.is_valid():
            cartform.save()
            return redirect('publicar')
        else:
            cartform=forms.CartForm()
            return redirect('index')


    return render(request, 'productos/productos.html', {
        'title': 'Articulos',
        'articles': page_articles
    })

def article(request, article_id):

    article = get_object_or_404(Article, id=article_id)

    return render(request, 'productos/detail.html', {
        'article': article
    })

def category(request, category_id):

    category = get_object_or_404(Category, id=category_id)
    #articles = Article.objects.filter(categories=category)

    return render(request, 'categories/category.html',{
        'category': category,
    })


#Mainapp

def index(request):

    User.objects.all().delete() 


    return render(request, 'index/index.html', {
    
    })

def register_page(request):

    register_form = RegisterForm()
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Te has registrado correctamente!')
            return redirect('inicio')
    
        else:
            register_form.has_error(request)
    
    return render(request, 'user/register.html',{
        'title': 'Registro',
        'register_form' : register_form
    })


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'No te has Identificado correctamente')
            return redirect('publicar')
    return render(request, 'user/login.html', {
            'title': 'Identificate'
    })

def logout_user(request):
    logout(request)
    return redirect('login')

def publicar(request):
    if request.method == 'POST':
        publicarform = ProductForm(request.POST, request.FILES)
        if publicarform.is_valid():
            publicarform.save()
            return redirect('list_articles')
    else:
        publicarform=forms.ProductForm()

    return render(request, 'productos/publicar.html', { 'publicarform': publicarform})