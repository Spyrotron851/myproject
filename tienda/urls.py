from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.list, name="index"),
    path('articulos/', views.list, name="list_articles"),
    path('ultimo-articulo/', views.last_visited_article, name='last_visited_article'),
    path('categoria/<int:category_id>/', views.category, name="category"),
    path('articulo/<int:article_id>/', views.article, name="article"),
    path('registro/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('eliminar_un_producto/<int:producto_id>/', views.eliminar_un_producto, name='eliminar_un_producto'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('resultados_busqueda/<str:title>/', views.resultados_busqueda, name='resultados_busqueda'),
    path('verificar-mensajes/', views.verificar_mensajes, name='verificar_mensajes'),
    path('restablecer-contador/', views.reset_notification_counter, name='restablecer-contador'),
    path('configuraciones/', views.configuraciones, name='configuraciones'),
    path('actualizar_posicion_cuadro/<int:category_id>/', views.actualizar_posicion_cuadro, name='actualizar_posicion_cuadro'),
    path('obtener-datos/', views.obtener_datos, name='obtener_datos'),
    path('carrito-final/', views.carrito_final, name='carrito-final'),
    path('realizar_pago_paypal/', views.realizar_pago_paypal, name='realizar_pago_paypal'),
    path('contactar-vendedor/', views.contactar_vendedor, name='contactar_vendedor'),
    path('contactar_whatsapp/', views.contactar_whatsapp, name='contactar_whatsapp'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product')
]