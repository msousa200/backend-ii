"""
URL configuration for hello_app.
"""
from django.urls import path
from . import views

app_name = 'hello_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.hello_api, name='hello_api'),
]
