from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnuncioViewSet, ProductoViewSet, CategoriaViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'anuncios', AnuncioViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'servicios', ServicioViewSet)  # Registrar el nuevo endpoint para Servicios

urlpatterns = [
    path('', include(router.urls)),
]
