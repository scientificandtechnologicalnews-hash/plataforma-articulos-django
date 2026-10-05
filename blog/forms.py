# blog/forms.py

from django import forms
from .models import Article, Review

class ArticleForm(forms.ModelForm):
    """
    Formulario para que los redactores envíen sus artículos a revisión o los guarden como borrador.
    """
    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'tags', 'cover_image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Título del artículo...',
                'style': 'width: 100%; padding: 0.5rem;'
            }),
            'slug': forms.TextInput(attrs={
                'placeholder': 'url-amigable-del-articulo',
                'style': 'width: 100%; padding: 0.5rem;'
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Escribe aquí el contenido completo de tu artículo...'
            }),
        }


class ReviewForm(forms.ModelForm):
    """
    Formulario para que los revisores/editores dejen feedback y aprueben o rechacen un artículo.
    """
    class Meta:
        model = Review
        fields = ['feedback', 'approved']
        widgets = {
            'feedback': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe los comentarios de revisión para el autor...'
            }),
        }

        