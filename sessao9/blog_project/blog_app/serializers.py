"""
Blog app serializers
"""
from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for the BlogPost model"""
    word_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'published_date', 
                  'is_published', 'author', 'category', 'word_count']
    
    def get_word_count(self, obj):
        """Get the word count from the BlogPost instance"""
        return obj.word_count()
