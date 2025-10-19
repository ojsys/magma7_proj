# Magma7Fitness - cPanel Deployment Guide

This guide will walk you through deploying your Django application to a cPanel hosting environment.

## Prerequisites

- cPanel account with Python support (3.8 or higher)
- SSH access to your cPanel account
- Domain name configured in cPanel
- MySQL database (recommended for production)

---

## Step 1: Prepare Your cPanel Environment

### 1.1 Create a Python Application in cPanel

1. Log in to your cPanel account
2. Navigate to **"Setup Python App"** or **"Python Selector"**
3. Click **"Create Application"**
4. Configure:
   - **Python Version**: 3.9 or higher
   - **Application Root**: `/home/username/magma7` (or your preferred directory)
   - **Application URL**: Your domain (e.g., `magma7fitness.com`)
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`

### 1.2 Create a MySQL Database

1. Go to **"MySQL Databases"** in cPanel
2. Create a new database (e.g., `username_magma7`)
3. Create a database user with a strong password
4. Add the user to the database with **ALL PRIVILEGES**
5. Note down the database name, username, password, and host

---

## Step 2: Upload Your Application Files

### Option A: Using File Manager (Easier)

1. In cPanel, go to **"File Manager"**
2. Navigate to your application root directory (e.g., `/home/username/magma7`)
3. Upload all your project files (you can zip them first for faster upload)
4. Extract the files if you uploaded a zip

### Option B: Using SSH/SCP (Recommended)

```bash
# From your local machine, upload files using SCP
scp -r /path/to/local/magma7 username@yourserver.com:/home/username/

# Or use rsync for better control
rsync -avz --exclude='venv' --exclude='*.pyc' --exclude='db.sqlite3' \
  /path/to/local/magma7/ username@yourserver.com:/home/username/magma7/
```

---

## Step 3: Configure Environment Variables

### 3.1 Create Production .env File

SSH into your server and create a `.env` file in your application directory:

```bash
ssh username@yourserver.com
cd /home/username/magma7
nano .env
```

Add the following configuration (update with your actual values):

```env
# Django Settings
DJANGO_SECRET_KEY=your-production-secret-key-here-make-it-long-and-random
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_NAME=username_magma7
DB_USER=username_magma7user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Payment Configuration
PAYMENTS_ENABLED=1
PAYMENT_PROVIDER=paystack
SITE_URL=https://yourdomain.com

# Paystack Configuration
PAYSTACK_PUBLIC_KEY=pk_live_your_live_public_key
PAYSTACK_SECRET_KEY=sk_live_your_live_secret_key

# Currency
CURRENCY=NGN

# Security
SECURE_SSL_REDIRECT=1
```

**Important**: Make sure to secure the .env file:
```bash
chmod 600 .env
```

### 3.2 Update settings.py for MySQL

Edit `magma7/settings.py` and uncomment the MySQL database configuration:

```python
# Comment out SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Uncomment MySQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'magma7_db'),
        'USER': os.getenv('DB_USER', 'magma7_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

---

## Step 4: Install Dependencies

### 4.1 Activate Virtual Environment

```bash
cd /home/username/magma7
source virtualenv/bin/activate
```

### 4.2 Install Python Packages

```bash
pip install -r requirements.txt

# If using MySQL, also install the MySQL client
pip install mysqlclient
```

**Note**: If you encounter issues with `mysqlclient`, you may need to install system dependencies:
```bash
# Contact your hosting provider if you don't have sudo access
sudo yum install mysql-devel python3-devel gcc  # For CentOS/RHEL
# OR
sudo apt-get install libmysqlclient-dev python3-dev  # For Ubuntu/Debian
```

---

## Step 5: Update passenger_wsgi.py Paths

Edit `passenger_wsgi.py` and update the paths to match your cPanel directory structure:

```python
# Update this line to match your actual path
project_home = '/home/username/magma7'  # Replace 'username' with your actual cPanel username

# Update virtual environment path
VIRTUALENV = '/home/username/virtualenv/magma7/3.9/bin/activate_this.py'
```

---

## Step 6: Initialize Database

### 6.1 Run Migrations

```bash
cd /home/username/magma7
source virtualenv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6.3 Create Initial Data (Optional)

If you have fixtures or want to create initial plans:

```bash
python manage.py shell
```

Then create your membership plans:

```python
from memberships.models import Plan

Plan.objects.create(
    name='Monthly',
    price=25000,
    duration_days=30,
    is_active=True,
    is_featured=False
)

Plan.objects.create(
    name='Quarterly',
    price=65000,
    duration_days=90,
    is_active=True,
    is_featured=True
)

Plan.objects.create(
    name='Annual',
    price=200000,
    duration_days=365,
    is_active=True,
    is_featured=False
)
```

---

## Step 7: Collect Static Files

```bash
cd /home/username/magma7
source virtualenv/bin/activate
python manage.py collectstatic --noinput
```

This will copy all static files to the `staticfiles` directory.

---

## Step 8: Configure Static Files Serving

### 8.1 Update cPanel Static Files Configuration

In cPanel Python App settings:
- **Static files**: `/static/` → `/home/username/magma7/staticfiles/`
- **Static files**: `/media/` → `/home/username/magma7/media/`

### 8.2 Create Media Directory

```bash
mkdir -p /home/username/magma7/media
chmod 755 /home/username/magma7/media
```

---

## Step 9: Restart the Application

In cPanel:
1. Go to **"Setup Python App"**
2. Find your application
3. Click **"Restart"** or **"Stop/Start"**

Or via command line:
```bash
touch /home/username/magma7/tmp/restart.txt
```

---

## Step 10: Test Your Application

1. Visit your domain: `https://yourdomain.com`
2. Test the admin panel: `https://yourdomain.com/admin`
3. Test user registration and login
4. Test payment flow with test keys first
5. Check error logs if something doesn't work:
   ```bash
   tail -f /home/username/magma7/logs/django_errors.log
   ```

---

## Step 11: Configure SSL Certificate (HTTPS)

### 11.1 Install SSL Certificate in cPanel

1. Go to **"SSL/TLS Status"** in cPanel
2. Click **"Run AutoSSL"** for free Let's Encrypt certificate
3. OR upload your own SSL certificate

### 11.2 Update .env for SSL

Once SSL is active, update your `.env`:
```env
SECURE_SSL_REDIRECT=1
SITE_URL=https://yourdomain.com
```

Then restart the application.

---

## Step 12: Configure Cron Jobs (Optional but Recommended)

### 12.1 Session Cleanup

Add a cron job to clean expired sessions:

```bash
0 3 * * * cd /home/username/magma7 && source virtualenv/bin/activate && python manage.py clearsessions
```

### 12.2 Subscription Status Updates

Add a cron job to update subscription statuses:

```bash
0 4 * * * cd /home/username/magma7 && source virtualenv/bin/activate && python manage.py shell -c "from memberships.utils import update_subscription_statuses; update_subscription_statuses()"
```

To add cron jobs:
1. Go to **"Cron Jobs"** in cPanel
2. Add the commands with desired schedule

---

## Troubleshooting

### Application Returns 500 Error

1. Check error logs:
   ```bash
   tail -f /home/username/magma7/logs/django_errors.log
   ```

2. Check Passenger logs:
   ```bash
   tail -f /home/username/logs/passenger.log
   ```

3. Verify DEBUG is set to 0 in production

### Static Files Not Loading

1. Verify collectstatic was run successfully
2. Check static file paths in cPanel Python App settings
3. Verify file permissions (755 for directories, 644 for files)

### Database Connection Errors

1. Verify database credentials in .env
2. Test database connection:
   ```bash
   python manage.py dbshell
   ```

3. Check if database user has proper permissions

### Import Errors

1. Verify all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Check Python version matches requirements

### Permission Errors

1. Set proper permissions:
   ```bash
   chmod -R 755 /home/username/magma7
   chmod 600 /home/username/magma7/.env
   chmod -R 777 /home/username/magma7/media
   chmod -R 777 /home/username/magma7/logs
   ```

---

## Production Checklist

Before going live, verify:

- [ ] DEBUG = 0 in production .env
- [ ] SECRET_KEY is unique and secret
- [ ] ALLOWED_HOSTS is properly configured
- [ ] Database is MySQL (not SQLite)
- [ ] SSL certificate is installed
- [ ] All static files collected
- [ ] Payment provider keys are LIVE keys (not test)
- [ ] Email settings are configured and tested
- [ ] Superuser account created
- [ ] Initial plans created
- [ ] Error logging is working
- [ ] Backup strategy in place
- [ ] .env file is secure (chmod 600)

---

## Maintenance

### Updating the Application

1. SSH into server
2. Navigate to application directory
3. Pull latest code (if using git) or upload new files
4. Activate virtual environment
5. Install any new dependencies
6. Run migrations
7. Collect static files
8. Restart application

```bash
cd /home/username/magma7
source virtualenv/bin/activate
git pull origin main  # If using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

### Database Backups

Regular backups are crucial. Use cPanel's backup tools or set up automated backups:

```bash
# Example backup script
mysqldump -u username_magma7user -p username_magma7 > backup_$(date +%Y%m%d).sql
```

---

## Support

For issues:
1. Check Django logs: `/home/username/magma7/logs/django_errors.log`
2. Check Passenger logs: `/home/username/logs/passenger.log`
3. Review this deployment guide
4. Contact your hosting provider for server-specific issues

---

## Additional Resources

- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Passenger Documentation: https://www.phusionpassenger.com/docs/
- cPanel Documentation: https://docs.cpanel.net/

---

**Last Updated**: October 2025
**Version**: 1.0
