"""
WSGI config for magma7 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Use production settings by default for WSGI
# Override by setting DJANGO_SETTINGS_MODULE in your environment or passenger_wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.production')

application = get_wsgi_application()

