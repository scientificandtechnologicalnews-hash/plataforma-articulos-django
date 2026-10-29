# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('', views.article_list, name='article_list'),

    path('article/new/', views.article_create, name='article_create'),

    path('article/<slug:slug>/', views.article_detail, name='article_detail'),

    
    # Ruta para procesar el envío de comentarios
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),

    # Ruta para dar/quitar Me gusta
    path('article/<slug:slug>/like/', views.article_like, name='article_like'),
]


