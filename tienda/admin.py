from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Article, ContadorNotificaciones, VendedorConfiguracion, UserProfile

class CategoryAdmin(admin.ModelAdmin,):
    readonly_fields = ('created_at',)
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user',)   

class ContadorNotificacionesAdmin(admin.ModelAdmin):
    def contador(self, obj):
        try:
            return obj.contador
        except ContadorNotificaciones.DoesNotExist:
            return 0

    list_display = ('usuario', 'contador')

class VendedorConfiguracionAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'direccion', 'tiendafisica_tf', 'horario_atencion']
    search_fields = ['user__username', 'telefono', 'direccion']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'paypal_account',]

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin) 
admin.site.register(ContadorNotificaciones, ContadorNotificacionesAdmin)
admin.site.register(VendedorConfiguracion, VendedorConfiguracionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

