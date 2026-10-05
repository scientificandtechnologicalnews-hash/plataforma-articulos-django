# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Category, Tag
from .forms import ArticleForm


def article_list(request):
    """
    Vista pública de la portada: Muestra únicamente los artículos aprobados 
    y en estado 'PUBLICADO' (PUBLISHED).
    """
    articles = Article.objects.filter(status=Article.Status.PUBLISHED)
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug):
    """
    Vista detallada de un artículo específico a través de su 'slug' único.
    Solo muestra artículos que estén en estado 'PUBLICADO'.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
    return render(request, 'blog/article_detail.html', {'article': article})


@login_required
def article_create(request):
    """
    Vista protegida para que un redactor envíe un nuevo artículo.
    El artículo se guarda por defecto en estado 'PENDIENTE' (PENDING) para su revisión editorial.
    """
    if request.method == 'POST':
        # Pasamos request.FILES para soportar la carga de la imagen de portada
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user # Asignamos al usuario autenticado como autor
            article.status = Article.Status.PENDING # Se envía al flujo de revisión
            article.save()
            form.save_m2m() # Guarda las relaciones ManyToMany (Etiquetas / Tags)
            messages.success(
                request, 
                '¡Artículo enviado a revisión con éxito! Un editor lo evaluará antes de su publicación.'
            )
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'blog/article_form.html', {'form': form})

# Create your views here.
