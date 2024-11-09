from rest_framework import serializers  # type: ignore
from .models import Anuncio, Producto, Categoria, Servicio, Moneda

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['id', 'imagen', 'titulo']

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'titulo', 'imagen', 'telefono']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = ['id', 'nombre', 'tasa_cambio']

class ProductoSerializer(serializers.ModelSerializer):
    categorias_negocio = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categoria.objects.all()
    )
    precio_final = serializers.SerializerMethodField()
    precios_convertidos = serializers.SerializerMethodField()  # Field for converted prices

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio_normal', 'precio_nuevo', 'imagen',
            'es_nuevo', 'es_rebaja', 'domicilio_disponible', 'disponible', 
            'categorias_negocio', 'valoracion', 'precio_final', 'precios_convertidos'
        ]

    def get_precio_final(self, obj):
        """Calculate the final price based on the available prices."""
        return obj.precio_nuevo if obj.precio_nuevo else obj.precio_normal

    def get_precios_convertidos(self, obj):
        """Calculate the product's price in each currency based on the exchange rates."""
        # Get the base price in CUP, considering rebaja (precio_nuevo) if available
        base_price = self.get_precio_final(obj)
        
        # Get all currencies and calculate the converted prices
        precios = {}
        for moneda in Moneda.objects.all():
            precios[moneda.nombre] = {
                'precio_final': round(base_price / moneda.tasa_cambio, 2)
            }
            if obj.precio_nuevo:
                precios[moneda.nombre]['precio_rebaja'] = round(obj.precio_normal / moneda.tasa_cambio, 2)

        return precios
