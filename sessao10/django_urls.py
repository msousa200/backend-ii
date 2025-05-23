"""
Configuração de URLs para o projeto Django seguro.
Este arquivo seria normalmente urls.py em um projeto Django real.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


from secure_app.views import (
    register_user, 
    user_login, 
    user_logout,
    send_message,
    inbox,
    dashboard
)


urlpatterns = [

    path('secretadmin/', admin.site.urls),

    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/inbox/', inbox, name='inbox'),
    

    path('', RedirectView.as_view(url='/login/'), name='root'),
    

    path('locked-out/', RedirectView.as_view(
        url='/login/?locked=true'), 
        name='locked_out'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
