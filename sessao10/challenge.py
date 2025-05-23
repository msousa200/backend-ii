"""
Este módulo demonstra como implementar medidas de segurança abrangentes
em uma aplicação Django, incluindo proteção CSRF, gerenciamento seguro
de sessões e validação de entrada.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
import re
import bleach
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='security.log'
)
logger = logging.getLogger('security')


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Modelo para armazenar informações adicionais do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class SecureMessage(models.Model):
    """Modelo para armazenar mensagens seguras entre usuários"""
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.subject}"


from django import forms
from django.contrib.auth.forms import UserCreationForm

class SecureUserCreationForm(UserCreationForm):
    """Formulário seguro para criação de usuários com validação adicional"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_username(self):
        """Validação personalizada para nome de usuário"""
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        return username
    
    def clean_email(self):
        """Validação de email para garantir que é único"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

class SecureMessageForm(forms.ModelForm):
    """Formulário para envio de mensagens seguras"""
    class Meta:
        model = SecureMessage
        fields = ('recipient', 'subject', 'content')
    
    def clean_content(self):
        """Sanitiza o conteúdo da mensagem para prevenir XSS"""
        content = self.cleaned_data.get('content')
        sanitized_content = bleach.clean(
            content,
            tags=['p', 'b', 'i', 'u', 'em', 'strong'],
            attributes={},
            strip=True
        )
        return sanitized_content


@csrf_protect
def register_user(request):
    """View para registrar um novo usuário com proteção CSRF"""
    if request.method == 'POST':
        form = SecureUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            logger.info(f"New user registration: {user.username}")
            user.save()
            
            UserProfile.objects.create(user=user)
            
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = SecureUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@csrf_protect
def user_login(request):
    """View de login com proteção CSRF e limitação de tentativas"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        login_attempts = request.session.get('login_attempts', 0)
        if login_attempts >= 5:
            logger.warning(f"Too many login attempts for username: {username}")
            messages.error(request, "Too many login attempts. Please try again later.")
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['login_attempts'] = 0
            
        
            request.session.cycle_key()
            
            request.session.set_expiry(3600)  
            
            logger.info(f"Successful login: {username}")
            return redirect('dashboard')
        else:
            request.session['login_attempts'] = login_attempts + 1
            
            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

@login_required
@csrf_protect
def send_message(request):
    """View para enviar mensagens seguras entre usuários"""
    if request.method == 'POST':
        form = SecureMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            
            logger.info(f"Message sent from {request.user.username} to {message.recipient.username}")
            messages.success(request, "Message sent successfully.")
            return redirect('inbox')
    else:
        form = SecureMessageForm()
    
    return render(request, 'send_message.html', {'form': form})

@login_required
def inbox(request):
    """View para exibir mensagens recebidas"""
    user_messages = SecureMessage.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    return render(request, 'inbox.html', {'messages': user_messages})

from django.urls import path

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/inbox/', inbox, name='inbox'),
]

