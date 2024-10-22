from rest_framework import serializers
from .models import Anuncio, Producto, Categoria, Servicio

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['id', 'imagen', 'titulo']


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio  # Corregido para apuntar al modelo correcto
        fields = ['id', 'titulo', 'imagen', 'telefono']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    categorias_negocio = CategoriaSerializer(many=True)  # Maneja categorías anidadas.
    imagen = serializers.ImageField(required=False)
    precio_final = serializers.SerializerMethodField()  # Campo adicional de solo lectura para el precio final.

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio_normal', 'precio_nuevo', 'imagen',
            'es_nuevo', 'es_rebaja', 'domicilio_disponible', 'disponible', 
            'categorias_negocio', 'valoracion', 'precio_final'
        ]

    def get_precio_final(self, obj):
        """Devuelve el precio final basado en los campos de precios."""
        return obj.precio_nuevo if obj.precio_nuevo else obj.precio_normal

    def create(self, validated_data):
        # Extraer datos anidados de categorías
        categorias_data = validated_data.pop('categorias_negocio')
        
        # Crear el objeto Producto
        producto = Producto.objects.create(**validated_data)
        
        # Agregar las categorías relacionadas
        for categoria_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(**categoria_data)
            producto.categorias_negocio.add(categoria)
        
        return producto

    def update(self, instance, validated_data):
        # Extraer datos de categorías si se proporcionan
        categorias_data = validated_data.pop('categorias_negocio', None)
        
        # Actualizar los campos del producto
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio_normal = validated_data.get('precio_normal', instance.precio_normal)
        instance.precio_nuevo = validated_data.get('precio_nuevo', instance.precio_nuevo)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        instance.es_nuevo = validated_data.get('es_nuevo', instance.es_nuevo)
        instance.es_rebaja = validated_data.get('es_rebaja', instance.es_rebaja)
        instance.domicilio_disponible = validated_data.get('domicilio_disponible', instance.domicilio_disponible)
        instance.disponible = validated_data.get('disponible', instance.disponible)
        instance.valoracion = validated_data.get('valoracion', instance.valoracion)
        instance.save()

        # Actualizar las categorías si se proporcionan
        if categorias_data:
            instance.categorias_negocio.clear()  # Limpiar las categorías actuales
            for categoria_data in categorias_data:
                categoria, created = Categoria.objects.get_or_create(**categoria_data)
                instance.categorias_negocio.add(categoria)

        return instance
