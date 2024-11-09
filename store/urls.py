from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnuncioViewSet, ProductoViewSet, CategoriaViewSet, ServicioViewSet, MonedaViewSet

router = DefaultRouter()
router.register(r'anuncios', AnuncioViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'monedas', MonedaViewSet)  # Register endpoint for Moneda

urlpatterns = [
    path('', include(router.urls)),
]
