"""
Tests for the Django Hello World application.

Run with: python manage.py test
"""
from django.test import TestCase, Client
from django.urls import reverse
import json


class HelloViewTests(TestCase):
    """Test cases for the hello_view API endpoint."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = Client()
    
    def test_hello_view_returns_success(self):
        """Test the hello view returns a successful response."""
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Hello, World!')
    
    def test_hello_view_with_name(self):
        """Test the hello view with a name parameter."""
        name = "TestUser"
        response = self.client.get(f"{reverse('hello')}?name={name}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], f'Hello, {name}!')
    
    def test_hello_view_with_invalid_method(self):
        """Test the hello view with an invalid HTTP method."""
        response = self.client.post(reverse('hello'))
        self.assertEqual(response.status_code, 405) 
