from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect  # Importamos redirect para hacer la redirección

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta de admin
    path('', lambda request: redirect('admin/')),  # Redirige la raíz al admin
    path('api/', include('store.urls')),  # Incluye las rutas de la app bajo 'anuncios/'
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
