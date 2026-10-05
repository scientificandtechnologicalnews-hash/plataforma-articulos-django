# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Vistas estándar de autenticación de Django (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Rutas de la plataforma de artículos
    path('', include('blog.urls')),
]

# Servir archivos de imagen subidos en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)