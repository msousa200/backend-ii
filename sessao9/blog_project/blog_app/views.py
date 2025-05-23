"""
Blog app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing blog posts
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        """
        Optionally filter by published status
        """
        queryset = BlogPost.objects.all()
        is_published = self.request.query_params.get('published', None)
        
        if is_published is not None:
            is_published = is_published.lower() == 'true'
            queryset = queryset.filter(is_published=is_published)
            
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Publish a blog post
        """
        post = self.get_object()
        post.publish()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """
        List posts by author
        """
        author = request.query_params.get('author', None)
        if author is None:
            return Response(
                {"error": "Author parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        posts = BlogPost.objects.filter(author=author)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
