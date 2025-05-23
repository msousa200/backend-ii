"""
Tests for the BlogPost model
"""
import pytest
from django.utils import timezone
from datetime import timedelta
import freezegun
from blog_app.models import BlogPost


@pytest.mark.django_db
class TestBlogPostModel:
    """Test suite for the BlogPost model"""
    
    def test_create_blog_post(self):
        """Test creating a blog post"""
        post = BlogPost.objects.create(
            title="Test Post",
            content="This is a test post content",
            author="Test Author"
        )
        
        assert post.title == "Test Post"
        assert post.content == "This is a test post content"
        assert post.author == "Test Author"
        assert post.is_published is False
        assert post.category == "General"
        
    def test_string_representation(self):
        """Test the string representation of a blog post"""
        post = BlogPost(title="Test Post")
        assert str(post) == "Test Post"
        
    def test_publish_method(self):
        """Test the publish method"""
        post = BlogPost.objects.create(
            title="Unpublished Post",
            content="This post is not published yet"
        )

        assert post.is_published is False
        
        with freezegun.freeze_time("2023-05-20 12:00:00"):
            frozen_time = timezone.now()
            post.publish()
            
            assert post.is_published is True
            assert post.published_date == frozen_time
            
            refreshed_post = BlogPost.objects.get(id=post.id)
            assert refreshed_post.is_published is True
            assert refreshed_post.published_date == frozen_time
            
    def test_word_count_method(self):
        """Test the word_count method"""
        post1 = BlogPost(title="Empty Post", content="")
        assert post1.word_count() == 0
        
        post2 = BlogPost(title="Single Word", content="Word")
        assert post2.word_count() == 1
        
        post3 = BlogPost(title="Multiple Words", 
                         content="This post has exactly five words")
        assert post3.word_count() == 5
        
        post4 = BlogPost(title="Complex Content", 
                         content="This post, with punctuation and    spacing, has 8 words!")
        assert post4.word_count() == 8
        
    @pytest.mark.parametrize(
        "title,content,expected_count",
        [
            ("Empty", "", 0),
            ("One", "Word", 1),
            ("Five", "One two three four five", 5),
            ("Spaces", "   Spaces   at   ends   ", 3),
        ]
    )
    def test_word_count_parametrized(self, title, content, expected_count):
        """Parametrized test for word_count with various inputs"""
        post = BlogPost(title=title, content=content)
        assert post.word_count() == expected_count
