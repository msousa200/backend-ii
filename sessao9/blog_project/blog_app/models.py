"""
Blog app models file
"""
from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    """
    Modelo que representa um post de blog.
    
    Atributos:
        title: Título do post
        content: Conteúdo do post
        published_date: Data de publicação
        is_published: Indica se o post está publicado
        author: Autor do post
        category: Categoria do post
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    author = models.CharField(max_length=100, default="Anonymous")
    category = models.CharField(max_length=50, default="General")
    
    def __str__(self):
        """Retorna uma representação em string do BlogPost."""
        return self.title
    
    def publish(self):
        """Publica o post definindo is_published como True."""
        self.is_published = True
        self.published_date = timezone.now()
        self.save()
    
    def word_count(self):
        """Retorna o número de palavras no conteúdo."""
        return len(self.content.split())
