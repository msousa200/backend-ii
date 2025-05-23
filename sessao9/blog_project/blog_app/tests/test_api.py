"""
Tests for the BlogPost API endpoints
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from blog_app.models import BlogPost
import json
import freezegun
from django.utils import timezone


@pytest.fixture
def api_client():
    """Return an authenticated API client"""
    return APIClient()


@pytest.fixture
def sample_posts():
    """Create sample blog posts for testing"""
    with freezegun.freeze_time("2023-05-15 10:00:00"):
        posts = [
            BlogPost.objects.create(
                title="Published Post 1",
                content="Content of published post 1",
                author="John Doe",
                category="Tech",
                is_published=True
            ),
            BlogPost.objects.create(
                title="Published Post 2",
                content="Content of published post 2",
                author="Jane Smith",
                category="Tech",
                is_published=True
            ),
            BlogPost.objects.create(
                title="Unpublished Post",
                content="This post is not published yet",
                author="John Doe",
                category="Health",
                is_published=False
            ),
        ]
    return posts


@pytest.mark.django_db
class TestBlogPostAPI:
    """Test suite for the BlogPost API"""
    
    def test_list_posts(self, api_client, sample_posts):
        """Test listing all blog posts"""
        url = reverse('blogpost-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3 
    
    def test_filter_published_posts(self, api_client, sample_posts):
        """Test filtering posts by published status"""
        url = reverse('blogpost-list')
        response = api_client.get(f"{url}?published=true")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  
        
        for post in response.data['results']:
            assert post['is_published'] is True
    
    def test_filter_by_category(self, api_client, sample_posts):
        """Test filtering posts by category"""
        url = reverse('blogpost-list')
        response = api_client.get(f"{url}?category=Tech")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  
        
        for post in response.data['results']:
            assert post['category'] == 'Tech'
    
    def test_retrieve_post(self, api_client, sample_posts):
        """Test retrieving a single blog post"""
        post = sample_posts[0]
        url = reverse('blogpost-detail', args=[post.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title
        assert response.data['content'] == post.content
        assert response.data['author'] == post.author
        assert response.data['word_count'] == post.word_count()
    
    def test_create_post(self, api_client):
        """Test creating a new blog post"""
        url = reverse('blogpost-list')
        data = {
            'title': 'New Test Post',
            'content': 'Content of new test post',
            'author': 'Test Creator',
            'category': 'News'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['content'] == data['content']
        assert response.data['author'] == data['author']
        assert response.data['category'] == data['category']
        assert response.data['is_published'] is False  
        
        post_id = response.data['id']
        post = BlogPost.objects.get(id=post_id)
        assert post.title == data['title']
    
    def test_update_post(self, api_client, sample_posts):
        """Test updating a blog post"""
        post = sample_posts[0]
        url = reverse('blogpost-detail', args=[post.id])
        data = {
            'title': 'Updated Title',
            'content': post.content,  
            'author': post.author,    
            'category': 'Updated Category'
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['category'] == 'Updated Category'
        
        post.refresh_from_db()
        assert post.title == 'Updated Title'
        assert post.category == 'Updated Category'
    
    def test_delete_post(self, api_client, sample_posts):
        """Test deleting a blog post"""
        post = sample_posts[0]
        url = reverse('blogpost-detail', args=[post.id])
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        with pytest.raises(BlogPost.DoesNotExist):
            BlogPost.objects.get(id=post.id)
    
    def test_publish_action(self, api_client, sample_posts):
        """Test the publish action"""
        post = sample_posts[2]  
        url = reverse('blogpost-publish', args=[post.id])
        
        with freezegun.freeze_time("2023-05-20 15:30:00"):
            frozen_time = timezone.now()
            response = api_client.post(url)
            
            assert response.status_code == status.HTTP_200_OK
            assert response.data['is_published'] is True
            
            post.refresh_from_db()
            assert post.is_published is True
            assert post.published_date == frozen_time
    
    def test_by_author_action(self, api_client, sample_posts):
        """Test the by_author action"""
        url = reverse('blogpost-by-author')
        
        response = api_client.get(f"{url}?author=John Doe")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  
        
        for post in response.data:
            assert post['author'] == 'John Doe'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
