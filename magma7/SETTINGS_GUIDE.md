# Django Settings Configuration Guide

Your Django project now uses **separate settings files** for different environments. This is a Django best practice that makes it easier to manage configuration across development and production.

---

## 📁 Settings Structure

```
magma7/
└── settings/
    ├── __init__.py          # Settings package initialization
    ├── base.py              # Common settings for all environments
    ├── development.py       # Development-specific settings
    └── production.py        # Production-specific settings
```

---

## 🎯 Settings Files Explained

### 1. `base.py` - Common Settings

Contains settings shared across ALL environments:
- Installed apps
- Middleware
- Templates configuration
- Static/media files configuration
- URL configuration
- Internationalization
- Payment provider settings (Paystack/Stripe)
- Email configuration variables

**What's NOT in base.py:**
- `SECRET_KEY` (defined in development.py and production.py)
- `DEBUG` (defined per environment)
- `ALLOWED_HOSTS` (defined per environment)
- `DATABASES` (defined per environment)
- Security settings (defined in production.py)

### 2. `development.py` - Development Settings

Settings for **local development**:
- `DEBUG = True`
- `ALLOWED_HOSTS = ['*']` (allows all hosts)
- SQLite database
- Console email backend (emails print to console)
- Detailed logging
- Development-friendly configuration

**Features:**
- Prints status message on startup
- Shows database file location
- Easier to debug

### 3. `production.py` - Production Settings

Settings for **production deployment**:
- `DEBUG = False`
- `ALLOWED_HOSTS` from environment variable (required!)
- MySQL/MariaDB database
- SMTP email backend
- Security headers (HTTPS, secure cookies, etc.)
- Error logging to files
- Performance optimizations
- Strict validation of required environment variables

**Features:**
- Validates required settings on startup
- Enhanced security
- Error notifications
- Log rotation
- Template caching

---

## 🚀 How to Use

### Local Development

**Option 1: Default (easiest)**
```bash
# manage.py defaults to development settings
python manage.py runserver
```

**Option 2: Explicit**
```bash
# Explicitly specify development settings
DJANGO_SETTINGS_MODULE=magma7.settings.development python manage.py runserver
```

**Option 3: Environment Variable (recommended)**
```bash
# Set environment variable (lasts for terminal session)
export DJANGO_SETTINGS_MODULE=magma7.settings.development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

### Production Deployment

**On cPanel via passenger_wsgi.py:**
```python
# passenger_wsgi.py automatically uses production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.production')
```

**Manual Commands on Server:**
```bash
# For any manage.py commands on production
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

**In .env file (production):**
```env
# Not needed - passenger_wsgi.py sets it automatically
# But you can add it for consistency:
DJANGO_SETTINGS_MODULE=magma7.settings.production
```

---

## 📝 Environment Variables

### Required for Development

None! Development works out of the box with defaults.

### Required for Production

These MUST be set in production `.env` file:

```env
# Django Core
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (MySQL)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Payment
PAYMENTS_ENABLED=1
PAYMENT_PROVIDER=paystack
SITE_URL=https://yourdomain.com
PAYSTACK_PUBLIC_KEY=pk_live_your_live_key
PAYSTACK_SECRET_KEY=sk_live_your_live_key
CURRENCY=NGN

# Security
SECURE_SSL_REDIRECT=1
```

---

## 🔍 Checking Your Settings

### Verify Which Settings Are Active

```bash
python -c "from django.conf import settings; print(settings.SETTINGS_MODULE)"
```

### Run Django System Check

**Development:**
```bash
DJANGO_SETTINGS_MODULE=magma7.settings.development python manage.py check
```

**Production:**
```bash
DJANGO_SETTINGS_MODULE=magma7.settings.production python manage.py check --deploy
```

### Check Database Configuration

```bash
python manage.py shell
```

Then in the shell:
```python
from django.conf import settings
print(f"Settings: {settings.SETTINGS_MODULE}")
print(f"DEBUG: {settings.DEBUG}")
print(f"Database: {settings.DATABASES['default']['ENGINE']}")
print(f"Database Name: {settings.DATABASES['default']['NAME']}")
```

---

## 🎨 Visual Indicators

Both settings files print helpful startup messages:

**Development:**
```
🚀 Running in DEVELOPMENT mode
📁 Database: /path/to/db.sqlite3
📧 Email backend: django.core.mail.backends.console.EmailBackend
```

**Production:**
```
🔒 Running in PRODUCTION mode
🌐 Allowed hosts: yourdomain.com, www.yourdomain.com
🗄️  Database: django.db.backends.mysql - your_database
📧 Email backend: django.core.mail.backends.smtp.EmailBackend
🔐 SSL Redirect: True
```

---

## ⚙️ Common Development Commands

All these work automatically with development settings:

```bash
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

---

## 🏭 Common Production Commands

On production server, use explicit settings:

```bash
# Set environment variable for session
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Then run commands
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Or one-liners
DJANGO_SETTINGS_MODULE=magma7.settings.production python manage.py migrate
```

---

## 🔐 Security Notes

### Development Settings
- `DEBUG = True` - Shows detailed error pages
- `ALLOWED_HOSTS = ['*']` - Accepts requests from any host
- SQLite database - File-based, easy to delete/reset
- Console email - No real emails sent
- **Never use in production!**

### Production Settings
- `DEBUG = False` - Hides sensitive information
- `ALLOWED_HOSTS` - Only accepts specific domains
- MySQL database - Persistent, production-grade
- SMTP email - Real emails sent
- Security headers enabled
- SSL/HTTPS enforced
- **Validates required settings on startup**

---

## 🐛 Troubleshooting

### "ImproperlyConfigured: Requested setting X, but settings are not configured"

**Cause**: Django can't find the settings module

**Solution**:
```bash
# Explicitly set the settings module
export DJANGO_SETTINGS_MODULE=magma7.settings.development
python manage.py runserver
```

### "ValueError: DJANGO_SECRET_KEY environment variable is required in production!"

**Cause**: Missing SECRET_KEY in production .env

**Solution**:
```bash
# Generate a new secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Add to .env
DJANGO_SECRET_KEY=generated-key-here
```

### "ValueError: DJANGO_ALLOWED_HOSTS environment variable is required in production!"

**Cause**: Missing ALLOWED_HOSTS in production .env

**Solution**:
```env
# Add to .env
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database connection errors in production

**Cause**: Missing or incorrect database credentials

**Solution**:
```env
# Verify all database settings in .env
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| **Development** | `python manage.py runserver` |
| **Production Check** | `DJANGO_SETTINGS_MODULE=magma7.settings.production python manage.py check --deploy` |
| **See Active Settings** | `python -c "from django.conf import settings; print(settings.SETTINGS_MODULE)"` |
| **Development Shell** | `python manage.py shell` |
| **Production Shell** | `DJANGO_SETTINGS_MODULE=magma7.settings.production python manage.py shell` |

---

## 🎯 Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use development settings locally** - Easier debugging
3. **Always use production settings on server** - Security
4. **Test with production settings before deploying** - Catch issues early
5. **Keep base.py DRY** - Don't repeat settings
6. **Document custom settings** - Help future you

---

## 📚 Additional Resources

- Django Settings Documentation: https://docs.djangoproject.com/en/stable/topics/settings/
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Environment Variables: https://12factor.net/config

---

**Your settings are now properly separated! 🎉**

- Development: Easy and convenient
- Production: Secure and validated
- Both: Well-organized and maintainable
