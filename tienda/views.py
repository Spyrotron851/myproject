from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from tienda.forms import ProductForm
from django.core.paginator import Paginator
#mainapp
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from tienda.forms import RegisterForm, VendedorConfiguracionForm, UserDataForm, PaymentForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Article, UserProfile, Carrito, ItemCarrito, Category, VendedorConfiguracion, ContadorNotificaciones
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ContadorNotificaciones
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Article
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseServerError
from .validators import CustomMinimumLengthValidator, CustomUserAttributeSimilarityValidator

import paypalrestsdk


@receiver(post_save, sender=User)
def create_contador_notificaciones(sender, instance, created, **kwargs):
    if created:
        ContadorNotificaciones.objects.create(usuario=instance)

# Create your views here


def list(request):
    articles = Article.objects.all()
    categories = Category.objects.all()

    # Paginar Articulos
    paginator = Paginator(articles, 100)
    page = request.GET.get('page')
    page_articles = paginator.get_page(page)

    data = ["Cuadro 1", "Cuadro 2", "Cuadro 3"]


    return render(request, 'productos/productos.html', {
        'title': 'Articulos',
        'articles': page_articles,
        'categories': categories,
        'data': data,
    })



def article(request, article_id):

    article = get_object_or_404(Article, id=article_id)
    category = article.categories
    
    # Guardar el ID del artículo visitado en la sesión
    request.session['last_article_id'] = article_id

    # Filtrar perfiles válidos por categoría y con cuentas de pago no vacías
    perfiles_validos = UserProfile.objects.filter(user__article__categories=category)

    # Inicializar una lista para almacenar las clases de pago existentes
    clases_de_pago = []
    envio = [str('Si')]

    if perfiles_validos.exclude(paypal_account='').exists():
        clases_de_pago.append("Paypal: Si")
    if perfiles_validos.exclude(whatsapp_account='').exists():
        clases_de_pago.append("Whatsapp: Si")
    if perfiles_validos.exclude(mail_account='').exists():
        clases_de_pago.append("Mail: Si")

    if VendedorConfiguracion.envio == True:
        envio.append("Si")

    # Unir las clases de pago en una sola cadena separada por comas
    clases_de_pago_str = " / ".join(clases_de_pago)

    return render(request, 'productos/detail.html', {
        'article': article,
        'category' : category,
        'clases_de_pago_str': clases_de_pago_str,
        'envio': envio,

    })

def last_visited_article(request):
    last_article_id = request.session.get('last_article_id', None)

    if last_article_id:
        return redirect('article', article_id=last_article_id)
    else:
        # Agregar un mensaje de alerta con una etiqueta personalizada
        messages.warning(request, 'No hay un artículo visitado recientemente.', extra_tags='no-article')
        return redirect('index')

def category(request, category_id):

    category = get_object_or_404(Category, id=category_id)
    #articles = Article.objects.filter(categories=category)

    return render(request, 'categories/category.html',{
        'category': category,
    })


#Mainapp

def index(request):

    return render(request, 'index/index.html', {
    
    })

def register_page(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Te has registrado y autenticado correctamente!')
            producto_id = request.session.pop('producto_id', None)
            if producto_id:
                return redirect('agregar_al_carrito', producto_id=producto_id)
            return redirect('index')
        else:
            # Manejo de errores específicos para password1
            if 'password1' in register_form.errors:
                for error in register_form.errors['password1']:
                    if 'min_length' in error:
                        messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                    elif 'similarity' in error:
                        messages.error(request, 'La contraseña es demasiado similar a tu información personal.')
                    else:
                        messages.error(request, error)
            
            # Manejo de errores específicos para password2
            if 'password2' in register_form.errors:
                for error in register_form.errors['password2']:
                    messages.error(request, error)

            # Agregar mensajes de error para otros campos
            for field, errors in register_form.errors.items():
                if field not in ['password1', 'password2']:
                    for error in errors:
                        messages.error(request, error)

    return render(request, 'user/register.html', {
        'title': 'Registro',
        'register_form': register_form,
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
            return redirect('login')
    return render(request, 'user/login.html', {
            'title': 'Identificate'
    })

def logout_user(request):
    logout(request)
    return redirect('login')


"""
def publicar(request):
    if request.method == 'POST':
        publicarform = ProductForm(request.POST, request.FILES)
        if publicarform.is_valid():
            publicarform.save()
            return redirect('list_articles')
    else:
        publicarform=forms.ProductForm()

    return render(request, 'productos/publicar.html', { 'publicarform': publicarform})

"""

def crear_producto(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        precio = request.POST.get('precio')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        user = request.user
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        producto = Article.objects.create(
            title=title,
            precio=precio,
            content=content, 
            image=image,
            user=user,
            categories=category,
        )

        return redirect('list_articles')
    else:
        categories = Category.objects.all()
        return render(request, 'carrito/crear_producto.html', {'categories': categories})


def agregar_al_carrito(request, producto_id):

    if not request.user.is_authenticated:
        # Guardar la URL del producto en la sesión para redirigir después de registro
        request.session['producto_id'] = producto_id
        return redirect('register')

    producto = get_object_or_404(Article, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar si el carrito tiene un contador_notificaciones asociado
    if not carrito.contador_notificaciones:
        contador_notificaciones = ContadorNotificaciones.objects.create(usuario=request.user)
        carrito.contador_notificaciones = contador_notificaciones
        carrito.save()

    # Obtener el contador actual antes de agregar el producto
    contador_anterior = carrito.contador_notificaciones.contador

    carrito.agregar_producto(producto)
    messages.success(request, f'Se ha agregado el producto {producto.title} al carrito. {carrito.contador_notificaciones}')

    # Actualizar el mensaje en el modelo ContadorNotificaciones
    if carrito.contador_notificaciones:
        nuevo_mensaje = f'Se ha agregado el producto {producto.title} al carrito. {carrito.contador_notificaciones.contador}'
        carrito.contador_notificaciones.mensaje = nuevo_mensaje
        carrito.contador_notificaciones.save()

        # Restaurar el valor del contador después de guardar los cambios
        carrito.contador_notificaciones.contador = contador_anterior + 1
        carrito.contador_notificaciones.save()

    return redirect('ver_carrito')


def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Article, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user)

    try:
        item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
        item.delete()
        
    except ItemCarrito.DoesNotExist:
        pass

    return redirect('ver_carrito')

def eliminar_un_producto(request, producto_id):
    producto = get_object_or_404(Article, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        item = ItemCarrito.objects.filter(carrito=carrito, producto_id=producto_id).first()
        if item:
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
                
            else:
                item.delete()
            

    return redirect('ver_carrito')

def ver_carrito(request):

    if request.user.is_authenticated:
        carrito_usuario, created = Carrito.objects.get_or_create(usuario=request.user)
        contador_notificaciones = carrito_usuario.contador_notificaciones
    else:
        contador_notificaciones = None
    

    try:
        carrito_usuario = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        carrito_usuario = Carrito.objects.create(usuario=request.user)

    items = carrito_usuario.itemcarrito_set.all()
    total = sum(item.cantidad * item.producto.precio for item in items)
    articulos = [item.get_producto() for item in items]  # Obtener las instancias de los artículos
    subtotal = sum(item.producto.precio for item in items)

    context = {
        'items': items,
        'total': total,
        'carrito_usuario': carrito_usuario,
        'articulos': articulos,
        'contador_notificaciones': contador_notificaciones,
        'subtotal': subtotal,
    }

    return render(request, 'carrito/ver_carrito.html', context)

def vaciar_carrito(request):
    carrito_usuario = Carrito.objects.get(usuario=request.user)
    carrito_usuario.productos.clear()
    messages.success(request, "El carrito se ha vaciado exitosamente.")
    return redirect('ver_carrito')

def carrito_final(request):
    try:
        carrito_usuario = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        carrito_usuario = Carrito.objects.create(usuario=request.user)

    items = carrito_usuario.itemcarrito_set.all()

    for item in items:
        subtotal_producto = item.cantidad * item.producto.precio
        item.subtotal = subtotal_producto
        item.save()

    total = sum(item.cantidad * item.producto.precio for item in items)
    subtotal = sum(item.subtotal for item in items)
    articulos = [item.get_producto() for item in items]  # Obtener las instancias de los artículos

    # Verificar si el vendedor de cada artículo tiene configurado el PayPal ID
    vendedores_con_paypal = set()
    vendedores_con_whatsapp = set()
    vendedores_con_mail = set()

    for item in items:
        vendedor = item.producto.user  # Obtener el usuario vendedor del artículo
        try:
            vendedor_profile = UserProfile.objects.get(user=vendedor)
            if vendedor_profile.paypal_account:
                vendedores_con_paypal.add(vendedor.username)
            if vendedor_profile.whatsapp_account:
                vendedores_con_whatsapp.add(vendedor.username)
            if vendedor_profile.mail_account:
                vendedores_con_mail.add(vendedor.username)
        except UserProfile.DoesNotExist:
            messages.error(request, f'El vendedor {vendedor.username} no tiene configurado el perfil.')

    # Determinar la disponibilidad de los métodos de pago según el perfil del vendedor
    paypal_available = bool(vendedores_con_paypal)
    whatsapp_available = bool(vendedores_con_whatsapp)
    mail_available = bool(vendedores_con_mail)

    # Obtener la URL de WhatsApp configurada por el primer vendedor con WhatsApp
    whatsapp_url = None
    if whatsapp_available:
        vendedor = items[0].producto.user  # Utiliza el primer vendedor que tenga WhatsApp configurado
        vendedor_profile = UserProfile.objects.get(user=vendedor)
        whatsapp_url = f"{vendedor_profile.whatsapp_account}?text=Buen%20Día,%20Quiero%20Comprar%20Artículos."

    context = {
        'carrito': carrito_usuario,
        'paypal_available': paypal_available,
        'whatsapp_available': whatsapp_available,
        'mail_available': mail_available,
        'whatsapp_url': whatsapp_url,

        'items': items,
        'total': total,
        'carrito_usuario': carrito_usuario,
        'articulos': articulos,
        'subtotal': subtotal,
    }

    return render(request, 'carrito/carrito-final.html', context)


def header(request):

    if request.user.is_authenticated:
        carrito_usuario, created = Carrito.objects.get_or_create(usuario=request.user)
        contador_notificaciones = carrito_usuario.contador_notificaciones
    else:
        contador_notificaciones = None

    # Obtener el carrito del usuario actual
    try:
        carrito_usuario = Carrito.objects.get(usuario=request.user)
        contador = carrito_usuario.itemcarrito_set.aggregate(Sum('cantidad')).get('cantidad__sum') or 0
    except Carrito.DoesNotExist:
        carrito_usuario = None
        contador = 0

    if request.method == 'POST':
        # Obtener el valor de búsqueda del formulario
        title = request.POST.get('title')
        if title is not None:
            # Filtrar los productos por título
            productos = Article.objects.filter(title__icontains=title)
            print(f'título de búsqueda: {title}')
            print(f'productos encontrados: {productos}')
        else:
            productos = None
            print(f'título de búsqueda: {title}')
            print(f'productos encontrados: {productos}')

        # Crear una lista con los datos de cada producto
        resultados = []
        for producto in productos:
            datos_producto = {
                'title': producto.title,
                'content': producto.content,
                'image_url': producto.image.url,
                'username': producto.user.username,
                'category': producto.categories.name,
                'precio': producto.precio,
            }
            resultados.append(datos_producto)
            print(f'producto agregado: {datos_producto}')



        return redirect('resultados_busqueda', title=title)

    return render(request, 'productos/header.html', {
        'contador_notificaciones': contador_notificaciones
    })


def buscar_productos(request):
    if request.method == 'POST':
        # Obtener el valor de búsqueda del formulario
        title = request.POST.get('title')
        if title is not None:
            # Filtrar los productos por título
            productos = Article.objects.filter(title__icontains=title)
            print(f'título de búsqueda: {title}')
            print(f'productos encontrados: {productos}')
        else:
            productos = None
            print(f'título de búsqueda: {title}')
            print(f'productos encontrados: {productos}')

        # Crear una lista con los datos de cada producto
        resultados = []
        for producto in productos:
            datos_producto = {
                'title': producto.title,
                'content': producto.content,
                'image': producto.image.url,
                'user': producto.user.username,
                'category': producto.categories.name,
                'precio': producto.precio,
            }
            resultados.append(datos_producto)
            print(f'producto agregado: {datos_producto}')

        # Renderizar la página de resultados de búsqueda
        return redirect('resultados_busqueda', title=title)

    return render(request, 'buscador/buscar_productos.html')

def resultados_busqueda(request, title):
    productos = Article.objects.filter(title__icontains=title)
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'buscador/resultados_busqueda.html', {
        'productos': productos,
        'categories': categories,

        
    })



def verificar_mensajes(request):
    contador_notificaciones = ContadorNotificaciones.objects.filter(usuario=request.user).distinct().first()
    mensaje_actual = contador_notificaciones.mensaje

    # Simula un valor de mensaje anterior diferente para la demostración

    context = {
        'mensaje_actual': mensaje_actual,
    }

    return render(request, 'productos/mensajes.html', context)

@require_POST
def reset_notification_counter(request):
    try:
        # Obtener el objeto ContadorNotificacion para el usuario actual
        contador_notificaciones = ContadorNotificaciones.objects.get(usuario=request.user)
        # Restablecer el contador a 0
        contador_notificaciones.contador = 0
        contador_notificaciones.save()
        return JsonResponse({'success': True})
    except ContadorNotificaciones.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El objeto ContadorNotificacion no existe para este usuario'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def configuraciones(request):
    # Obtener la configuración del vendedor y el perfil del usuario
    vendedor_configuracion, created = VendedorConfiguracion.objects.get_or_create(user=request.user)
    perfil_usuario, created = UserProfile.objects.get_or_create(user=request.user)

    # Filtrar los productos del usuario
    productos_usuario = Article.objects.filter(user=request.user)

    if request.method == 'POST':
        # Procesar los formularios enviados
        payment_form = PaymentForm(request.POST, instance=perfil_usuario)
        user_form = UserDataForm(request.POST, instance=request.user)
        vendedor_form = VendedorConfiguracionForm(request.POST, instance=vendedor_configuracion)

        # Manejo para la opción 4
        if 'guardar_opcion4' in request.POST:
            if payment_form.is_valid():
                payment_form.save()
                messages.success(request, 'Configuración de PayPal guardada exitosamente.')
            else:
                messages.error(request, 'Error al guardar la configuración de PayPal.')

        # Manejo para la opción 3
        elif 'guardar_opcion3' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Datos del usuario guardados exitosamente.')
            else:
                messages.error(request, 'Error al guardar los datos del usuario.')

        # Manejo para la opción 2 (productos)
        elif 'guardar_opcion2' in request.POST:
            product_id = request.POST.get('product_id')
            title = request.POST.get('title')
            precio = request.POST.get('precio')
            content = request.POST.get('content')
            image = request.FILES.get('image')
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)

            if product_id:
                # Editar producto existente
                producto = get_object_or_404(Article, id=product_id, user=request.user)
                producto.title = title
                producto.precio = precio
                producto.content = content

                # Solo actualizar la imagen si se sube una nueva
                if image:
                    producto.image = image

                producto.categories = category
                producto.save()
                messages.success(request, 'Producto actualizado exitosamente.')
            else:
                # Crear nuevo producto
                Article.objects.create(
                    title=title,
                    precio=precio,
                    content=content, 
                    image=image,
                    user=request.user,
                    categories=category,
                )
                messages.success(request, 'Producto creado exitosamente.')

        return redirect('configuraciones')
    else:
        # Cargar los formularios
        payment_form = PaymentForm(instance=perfil_usuario)
        user_form = UserDataForm(instance=request.user)
        vendedor_form = VendedorConfiguracionForm(instance=vendedor_configuracion)
        categories = Category.objects.all()

    # Obtener el mensaje más reciente
    latest_message = None
    message_storage = messages.get_messages(request)
    for message in message_storage:
        latest_message = message
        break

    # Renderizar la plantilla con el contexto
    return render(request, 'productos/configuraciones.html', {
        'vendedor_form': vendedor_form,
        'payment_form': payment_form,
        'user_form': user_form,
        'productos_usuario': productos_usuario,
        'categories': categories,
        'latest_message': latest_message,
    })


def actualizar_posicion_cuadro(request, category_id):
    if request.method == 'GET':
        # Aquí puedes agregar la lógica para actualizar la posición
        # Por ahora, simplemente retornamos una respuesta JSON
        return JsonResponse({'mensaje': 'Posición actualizada exitosamente'})
    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=400)
    
def obtener_datos(request):
    categoria_nombre = request.GET.get('categoria')
    productos_filtrados = Article.objects.filter(categories__name=categoria_nombre)

    productos_data = [
        {'id': producto.id, 'titulo': producto.title, 'precio': str(producto.precio)}
        for producto in productos_filtrados
    ]

    return JsonResponse({'productos': productos_data})

# PAYPAL
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a 'live' para producción
    "client_id": "AZlLMohunYVzspSXR2HNtTPSalh_cFQRoWZJ8VdM4V0Atog5VaajqSwKzAQ4Eeo-zVtj5p_G-hu97zjJ",
    "client_secret": "EHEdRviiJK-pyGw12tfelEKkGURTu0JEjNAtcOteGra3tCt2Gdcs0hzWNIpGfuii9tAPWl35Mv5ZNE1G"
})

def realizar_pago_paypal(request):
    # Obtener el carrito del usuario actual
    carrito_usuario = get_object_or_404(Carrito, usuario=request.user)
    # Obtener el primer artículo del carrito
    primer_item = carrito_usuario.itemcarrito_set.first()
    if not primer_item:
        return HttpResponse("Carrito vacío.", status=400)

    # Obtener el vendedor del primer artículo
    vendedor = primer_item.producto.user

    # Obtener el perfil del vendedor
    perfil_vendedor = get_object_or_404(UserProfile, user=vendedor)

    # Configurar PayPal con el ID de PayPal del vendedor
    paypalrestsdk.configure({
        "mode": "sandbox",  # Cambiar a 'live' para producción
        "client_id": perfil_vendedor.paypal_account,
        "client_secret": "EHEdRviiJK-pyGw12tfelEKkGURTu0JEjNAtcOteGra3tCt2Gdcs0hzWNIpGfuii9tAPWl35Mv5ZNE1G"
    })

    # Lógica de pago
    total = sum(item.cantidad * item.producto.precio for item in carrito_usuario.itemcarrito_set.all())
    payment = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "paypal"},
      "redirect_urls": {
        "return_url": "http://localhost:8000/payment/execute/",
        "cancel_url": "http://localhost:8000/"},
      "transactions": [{
        "item_list": {
          "items": [{
            "name": "Compra de carrito",
            "sku": "001",
            "price": str(total),
            "currency": "USD",
            "quantity": 1}]},
        "amount": {
          "total": str(total),
          "currency": "USD"},
        "description": "Descripción de la transacción"}]})

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        return HttpResponse(payment.error)
        
# Vista para contactar al vendedor
def contactar_vendedor(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']

            # Envía el correo
            send_mail(
                subject,
                message,
                sender,
                ['vendedor@example.com'],  # Correo del vendedor
            )

            messages.success(request, 'Correo enviado exitosamente.')
            return redirect('configuraciones')
    else:
        form = ContactForm()

    return render(request, 'productos/contactar_vendedor.html', {'form': form})


# Vista para contactar por WhatsApp
def contactar_whatsapp(request):
    # Lógica para contactar por WhatsApp
    return render(request, 'whatsapp_contact.html')


def ejecutar_pago(request):
    payer_id = request.GET.get('PayerID')
    payment_id = request.GET.get('paymentId')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return HttpResponse("Pago realizado con éxito")
    else:
        error_message = str(payment.error)
        return HttpResponseServerError(error_message)


def update_product(request, product_id):
    # Obtén el producto existente desde la base de datos
    product = get_object_or_404(Article, id=product_id)

    if request.method == 'POST':
        # Si el formulario ha sido enviado, procesa los datos recibidos
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Guarda los cambios en el producto
            form.save()
            # Redirecciona a alguna página de confirmación o a la misma página
            return redirect('configuraciones')  # Cambia 'configuraciones' por el nombre de tu vista
    else:
        # Si no es una solicitud POST, crea un formulario vacío para mostrar
        form = ProductForm(instance=product)

    # Renderiza la plantilla con el formulario y otros contextos necesarios
    return render(request, 'ruta_de_tu_plantilla.html', {'form': form})


