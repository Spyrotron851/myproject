from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('articulos/', views.list, name="list_articles"),
    path('categoria/<int:category_id>', views.category, name="category"),
    path('articulo/<int:article_id>', views.article, name="article"),
    path('publicar/', views.publicar, name="publicar"),
    path('registro/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),    


]