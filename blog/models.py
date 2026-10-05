# blog/models.py

from django.db import models
from django.conf import settings # Recomendado para ForeignKeys al modelo User de forma desacoplada


class Category(models.Model):
    """
    Categoría temática a la que pertenece un artículo (ej. Tecnología, Ciencia, Opinión).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (URL Amigable)")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Etiquetas secundarias para clasificar artículos con mayor flexibilidad.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre de la Etiqueta")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug (URL Amigable)")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return f'#{self.name}'


class Article(models.Model):
    """
    Modelo principal para representar los artículos. 
    Gestiona el ciclo de vida del contenido mediante un estado editorial (Borrador, Revisión, Publicado, Rechazado).
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        PENDING = 'PENDING', 'En Revisión'
        PUBLISHED = 'PUBLISHED', 'Publicado'
        REJECTED = 'REJECTED', 'Rechazado'

    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug para URL")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='articles', 
        verbose_name="Redactor / Autor"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='articles', 
        verbose_name="Categoría"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name="Etiquetas")
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True, verbose_name="Imagen de Portada")
    content = models.TextField(verbose_name="Contenido del Artículo")
    
    # Estado del artículo en el flujo editorial
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.DRAFT, 
        verbose_name="Estado Editorial"
    )
    
    # Trazabilidad de fechas
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Publicación")

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} [{self.get_status_display()}]'


class Review(models.Model):
    """
    Modelo para la administración editorial. Permite a los editores dejar notas de revisión
    y aprobar o rechazar un artículo enviado por un redactor.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews', verbose_name="Artículo")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews_given', 
        verbose_name="Revisor / Editor"
    )
    feedback = models.TextField(verbose_name="Comentarios de Revisión / Feedback")
    approved = models.BooleanField(default=False, verbose_name="¿Aprobado para Publicación?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Revisión")

    class Meta:
        verbose_name = "Revisión Editorial"
        verbose_name_plural = "Revisiones Editoriales"

    def __str__(self):
        return f'Revisión de {self.reviewer.username} para "{self.article.title}"'

# Create your models here.
