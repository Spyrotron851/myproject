from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Article, Prueba

class CategoryAdmin(admin.ModelAdmin,):
    readonly_fields = ('created_at',)
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)   

class PruebaAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin) 
admin.site.register(Prueba, PruebaAdmin) 