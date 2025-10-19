"""
Development settings for magma7 project.

Use this settings module for local development.
Set environment variable: DJANGO_SETTINGS_MODULE=magma7.settings.development
"""

from .base import *  # noqa
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend - console output for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development-specific logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Django Debug Toolbar (optional - uncomment if installed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Disable password validators in development for easier testing
# AUTH_PASSWORD_VALIDATORS = []

# Development-specific settings
# CORS_ALLOW_ALL_ORIGINS = True  # If using Django CORS headers

print("=" * 60)
print("DEVELOPMENT MODE - Django Application Starting")
print("=" * 60)
print(f"Database: {DATABASES['default']['NAME']}")
print(f"Email backend: {EMAIL_BACKEND}")
print("=" * 60)
