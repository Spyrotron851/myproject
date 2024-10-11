from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=255, verbose_name='Descripcion')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el:')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    content = models.CharField(max_length=150, verbose_name='Contenido')
    image = models.ImageField(default=None, verbose_name="Imagen", upload_to='articles')
    user = models.ForeignKey(User, verbose_name='Usuario', default=None, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, default=None, null=True, blank=True, verbose_name="Categorias", related_name="Articulos", on_delete=models.CASCADE)
    titlecart = models.CharField(max_length=100, verbose_name='TituloCart', null=True )
    contentcart = models.CharField(max_length=80, verbose_name='ContenidoCart', null=True)


    def __str__(self):
        return self.title

class Prueba(models.Model):
    title = models.CharField(max_length=150, verbose_name='TituloPrueba')
    content = models.CharField(max_length=150, verbose_name='ContenidoPrueba')
    image = models.ImageField(default=None, verbose_name="ImagenPrueba", upload_to='articles')
    user = models.ForeignKey(User, verbose_name='UsuarioPrueba', default=None, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, default=None, null=True, blank=True, verbose_name="CategoriasPrueba", related_name="Categ", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Productos(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titulo', null=True )
    content = models.CharField(max_length=80, verbose_name='Contenido', null=True)
    content2 = models.CharField(max_length=200, verbose_name='Contenido2', null=True)
    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'

    def __str__(self):
        return self.title
    