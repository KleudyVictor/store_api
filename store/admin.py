from django.contrib import admin
from .models import Anuncio, Producto, Categoria, Servicio

admin.site.register(Anuncio)
admin.site.register(Categoria)
admin.site.register(Servicio)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_normal', 'precio_nuevo', 'disponible')
    list_filter = ('disponible', 'categorias_negocio')
    search_fields = ('nombre',)
    filter_horizontal = ('categorias_negocio',)
