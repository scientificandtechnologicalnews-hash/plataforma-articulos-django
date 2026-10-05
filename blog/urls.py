# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Portada principal: listado de artículos publicados
    path('', views.article_list, name='article_list'),
    
    # Formulario para redactar y enviar un nuevo artículo
    path('article/new/', views.article_create, name='article_create'),
    
    # Vista pública detallada del artículo (ej. /article/mi-primer-articulo/)
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]
