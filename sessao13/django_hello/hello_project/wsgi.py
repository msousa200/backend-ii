"""
WSGI config for hello_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_project.settings')

application = get_wsgi_application()
