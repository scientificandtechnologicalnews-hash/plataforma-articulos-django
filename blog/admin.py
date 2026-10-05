# blog/admin.py

from django.contrib import admin
from .models import Category, Tag, Article, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración visual de categorías en el panel de administración.
    """
    list_display = ('name', 'slug')
    # Genera automáticamente el slug en el formulario del admin a partir del nombre
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Configuración visual de etiquetas en el panel de administración.
    """
    list_display = ('name', 'slug')
    # Genera automáticamente el slug en el formulario del admin a partir del nombre
    prepopulated_fields = {'slug': ('name',)}


class ReviewInline(admin.TabularInline):
    """
    Permite a los editores ver y añadir revisiones directamente 
    dentro de la vista de edición del mismo artículo.
    """
    model = Review
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Panel de administración editorial para gestionar el ciclo de vida de los artículos.
    """
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'published_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    # Auto-completa el slug con el título al redactar
    prepopulated_fields = {'slug': ('title',)} 
    # Muestra el bloque de revisiones incrustado en el artículo
    inlines = [ReviewInline] 
    actions = ['make_published']

    @admin.action(description='Aprobar y cambiar estado a PUBLICADO')
    def make_published(self, request, queryset):
        """
        Acción rápida en lote para que los editores aprueben múltiples artículos seleccionados.
        """
        queryset.update(status=Article.Status.PUBLISHED)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Gestión individual de las revisiones editoriales registradas.
    """
    list_display = ('article', 'reviewer', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('article__title', 'reviewer__username', 'feedback')

# Register your models here.
