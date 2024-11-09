from rest_framework import viewsets # type: ignore
from .models import Anuncio, Producto, Categoria, Servicio, Moneda
from .serializers import AnuncioSerializer, ProductoSerializer, CategoriaSerializer, ServicioSerializer, MonedaSerializer

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(disponible=True)
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class MonedaViewSet(viewsets.ModelViewSet):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializer
