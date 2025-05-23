"""
Blog app admin configuration
"""
from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin configuration for BlogPost model"""
    list_display = ('title', 'author', 'category', 'is_published', 'published_date')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
        ('Publication info', {
            'fields': ('author', 'category', 'is_published', 'published_date')
        }),
    )
