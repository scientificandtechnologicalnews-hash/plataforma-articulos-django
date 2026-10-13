# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Importaciones relativas explícitas recomendadas
from .models import Article, Category, Tag, Comment
from .forms import ArticleForm, CommentForm


def article_list(request):
    """
    Vista pública de la portada: Muestra únicamente los artículos aprobados 
    y en estado 'PUBLICADO' (PUBLISHED).
    """
    articles = Article.objects.filter(status=Article.Status.PUBLISHED)
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug):
    """
    Muestra el detalle del artículo publicado junto a sus comentarios existentes
    y el formulario para enviar uno nuevo.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
    comments = article.comments.all() # Obtiene todos los comentarios asociados al artículo
    comment_form = CommentForm() # Instancia el formulario limpio para redactar un comentario

    # Contexto explícito hacia la plantilla HTML
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/article_detail.html', context)


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