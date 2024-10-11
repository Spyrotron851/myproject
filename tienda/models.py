from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

   
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=255, verbose_name='Descripcion')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el:')
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True, verbose_name='Icono')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    content = models.CharField(max_length=1000, verbose_name='Contenido')
    image = models.ImageField(default=None, verbose_name="Imagen", upload_to='articles')
    user = models.ForeignKey(User, verbose_name='Usuario', default=None, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, default=None, null=True, blank=True, verbose_name="Categorias", related_name="Articulos", on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

@receiver(post_save, sender=Article)
def create_vendedor_configuracion(sender, instance, created, **kwargs):
    if created:
        VendedorConfiguracion.objects.get_or_create(user=instance.user)

# También puedes agregar una señal para actualizar la instancia de VendedorConfiguracion si el usuario cambia
@receiver(post_save, sender=User)
def update_vendedor_configuracion(sender, instance, created, **kwargs):
    if created:
        VendedorConfiguracion.objects.get_or_create(user=instance)
    else:
        vendedor_configuracion = VendedorConfiguracion.objects.filter(user=instance).first()
        if vendedor_configuracion:
            vendedor_configuracion.save()

class ContadorNotificaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contador = models.PositiveIntegerField(default=0)
    mensaje = models.CharField(max_length=200, default="Mensaje predeterminado")

    def __str__(self):
        return f'ContadorNotificaciones de {self.usuario.username}'
    
    @classmethod
    def get_mensaje_predeterminado(cls):
        # Método para obtener el mensaje predeterminado
        return cls._meta.get_field('mensaje').default

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Article, through='ItemCarrito')
    contador_notificaciones = models.OneToOneField(ContadorNotificaciones, null=True, blank=True, on_delete=models.CASCADE)

    def agregar_producto(self, producto):
        item, created = ItemCarrito.objects.get_or_create(carrito=self, producto=producto)
        print('item:', item)  # línea de depuración
        if not created:
            item.cantidad += 1
            item.save()
            print('cantidad actualizada:', item.cantidad)

        try:
            contador_notificaciones = ContadorNotificaciones.objects.get(usuario=self.usuario)
        except ObjectDoesNotExist:
            contador_notificaciones = ContadorNotificaciones.objects.create(usuario=self.usuario, contador=1)
        except ContadorNotificaciones.MultipleObjectsReturned:
            contador_notificaciones = ContadorNotificaciones.objects.filter(usuario=self.usuario).first()

        contador_notificaciones.contador += 1
        contador_notificaciones.save()
            
    def eliminar_producto(self, producto):
        item = ItemCarrito.objects.filter(carrito=self, producto=producto).first()
        if item:
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else:
                item.delete()
                
                contador_notificaciones = ContadorNotificaciones.objects.filter(usuario=self.usuario).first()
                if contador_notificaciones:
                    contador_notificaciones.contador -= 1
                    contador_notificaciones.save()

    def eliminar_todos_productos(self):
        items = ItemCarrito.objects.filter(carrito=self)
        cantidad_total = 0
        for item in items:
            cantidad_total += item.cantidad
            item.delete()

        # Agregar cantidad_total al contador de notificaciones
        contador_notificaciones = ContadorNotificaciones.objects.filter(usuario=self.usuario).first()
        if contador_notificaciones:
            contador_notificaciones.contador += cantidad_total
            contador_notificaciones.save()

        
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Article, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def get_producto(self):
        return self.producto
    
class VendedorConfiguracion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    tiendafisica_tf = models.BooleanField(default=False)
    horario_atencion = models.CharField(max_length=100, blank=True)
    envio = models.BooleanField(default=False)

    # Puedes agregar más campos según la información que desees almacenar

    def __str__(self):
        return self.user.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paypal_account = models.CharField(max_length=100, blank=True, null=True, verbose_name='Paypal ID')
    whatsapp_account = models.CharField(max_length=100, blank=True, null=True, verbose_name='Whatsapp')
    mail_account = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mail')
    def __str__(self):
        return self.user.username

