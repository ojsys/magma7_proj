import os
from pathlib import Path

# --- Simple .env loader (no external deps) ---
def _load_dotenv(env_path: Path):
    try:
        if env_path.exists():
            with env_path.open('r') as f:
                for raw in f.readlines():
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                        value = value[1:-1]
                    # Do not override if already set in environment
                    os.environ.setdefault(key, value)
    except Exception:
        # Non-fatal if .env cannot be read
        pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Since settings is now a package, we need to go up one more level
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env located at project root (next to manage.py)
_load_dotenv(BASE_DIR / '.env')

# SECRET_KEY, DEBUG, and ALLOWED_HOSTS are defined in environment-specific settings
# See settings/development.py and settings/production.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Local apps
    'core.apps.CoreConfig',
    'memberships.apps.MembershipsConfig',
    'notifications.apps.NotificationsConfig',
    'users.apps.UsersConfig',
    'payments.apps.PaymentsConfig',
    'cms.apps.CmsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.ErrorLoggingMiddleware',
    'cms.middleware.Custom404Middleware',
]

ROOT_URLCONF = 'magma7.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.unread_notifications',
                'core.context_processors.settings_vars',
                'cms.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'magma7.wsgi.application'

# DATABASES configuration is defined in environment-specific settings
# See settings/development.py and settings/production.py

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects
LOGIN_REDIRECT_URL = 'memberships:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# Email settings (console by default)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', '1') == '1'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@magma7fitness.local')

SITE_NAME = 'Magma7Fitness'

# Payments
PAYMENTS_ENABLED = os.getenv('PAYMENTS_ENABLED', '1') == '1'  # Enabled by default
PAYMENT_PROVIDER = os.getenv('PAYMENT_PROVIDER', 'paystack')  # 'paystack' or 'stripe'
SITE_URL = os.getenv('SITE_URL', 'http://127.0.0.1:8000')
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY', 'pk_test_96b9995fbf552beec8da11acbb821aa5c1d06341')  # Replace with your test key
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY', 'sk_test_96b9995fbf552beec8da11acbb821aa5c1d06341')  # Replace with your test key
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
CURRENCY = os.getenv('CURRENCY', 'NGN')

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
