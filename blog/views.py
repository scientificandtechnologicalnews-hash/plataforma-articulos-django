# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Importaciones relativas explícitas recomendadas
from .models import Article, Category, Tag, Comment
from .forms import ArticleForm, CommentForm


def article_list(request):
    """
    Vista pública de la portada: Filtra artículos aprobados (PUBLISHED)
    y permite búsquedas por texto, categoría o etiqueta.
    """
    articles = Article.objects.filter(status=Article.Status.PUBLISHED)

    # Filtrar por Categoría (si viene el parámetro ?category=slug en la URL)
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    # Filtrar por Etiqueta (si viene el parámetro ?tag=slug en la URL)
    tag_slug = request.GET.get('tag')
    if tag_slug:
        articles = articles.filter(tags__slug=tag_slug)

    # Búsqueda por palabra clave en título o contenido (?q=busqueda)
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'query': query,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    """
    Vista detallada del artículo publicado, comentarios e información de 'Me gusta'.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
    comments = article.comments.all()
    comment_form = CommentForm()

    # Comprobar si el usuario actual ya le dio 'Me gusta'
    is_liked = False
    if request.user.is_authenticated:
        is_liked = article.likes.filter(id=request.user.id).exists()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
    }
    return render(request, 'blog/article_detail.html', context)


@login_required
def article_like(request, slug):
    """
    Alterna la reacción 'Me gusta' del usuario activo en el artículo especificado.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)

    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user) # Si ya le gustaba, lo quita
    else:
        article.likes.add(request.user) # Si no, lo añade

    return redirect('article_detail', slug=slug)

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


@login_required
def add_comment(request, slug):
    """
    Procesa el envío de un nuevo comentario asociándolo al artículo y al usuario autenticado.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article # Relacionamos el comentario con este artículo
            comment.author = request.user # Relacionamos el comentario con el usuario autenticado
            comment.save()
            messages.success(request, '¡Tu comentario ha sido publicado!')
            
    return redirect('article_detail', slug=slug)