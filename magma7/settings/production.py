"""
Production settings for magma7 project.

Use this settings module for production deployment on cPanel.
Set environment variable: DJANGO_SETTINGS_MODULE=magma7.settings.production
"""

from .base import *  # noqa
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a new one: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is required in production!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS must be properly configured in production
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("DJANGO_ALLOWED_HOSTS environment variable is required in production!")

# Database - MySQL/MariaDB for production
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# Validate required database settings
required_db_settings = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
for setting in required_db_settings:
    if not os.getenv(setting):
        raise ValueError(f"{setting} environment variable is required in production!")

# Security Settings
# https://docs.djangoproject.com/en/stable/ref/settings/#security

# HTTPS/SSL
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '1') == '1'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# HSTS - HTTP Strict Transport Security
# Enable after SSL is fully configured and tested
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '0'))
if SECURE_HSTS_SECONDS > 0:
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# CSRF protection
CSRF_COOKIE_HTTPONLY = True

# Password validation - strict in production
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django_errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Admin notifications
ADMINS = [
    ('Admin', os.getenv('ADMIN_EMAIL', 'admin@example.com')),
]
MANAGERS = ADMINS

# Email configuration - use SMTP in production
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# Performance optimizations
# Static file storage with caching
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Template caching
if not DEBUG:
    for template_engine in TEMPLATES:
        if template_engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
            # When setting custom loaders, APP_DIRS must be False
            template_engine['APP_DIRS'] = False
            template_engine.setdefault('OPTIONS', {})
            template_engine['OPTIONS']['loaders'] = [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ]

print("=" * 60)
print("PRODUCTION MODE - Django Application Starting")
print("=" * 60)
print(f"Allowed hosts: {', '.join(ALLOWED_HOSTS)}")
print(f"Database: {DATABASES['default']['ENGINE']} - {DATABASES['default']['NAME']}")
print(f"Email backend: {EMAIL_BACKEND}")
print(f"SSL Redirect: {SECURE_SSL_REDIRECT}")
print("=" * 60)
