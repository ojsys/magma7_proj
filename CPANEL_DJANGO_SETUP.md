# Complete cPanel Django Deployment Guide

## Prerequisites
- cPanel access
- SSH access to your server
- Domain name pointed to your cPanel server

---

## Step-by-Step Setup Process

### 1. Upload Your Django Project

Upload your entire Django project to your home directory (NOT public_html):

```
/home/username/magma7_proj/
```

**Structure should be:**
```
/home/username/
├── magma7_proj/              # ← Your Django project goes here
│   ├── manage.py
│   ├── passenger_wsgi.py
│   ├── magma7/
│   ├── core/
│   ├── memberships/
│   ├── users/
│   ├── payments/
│   ├── cms/
│   ├── notifications/
│   ├── requirements.txt
│   └── .env
└── public_html/              # ← Web root (already exists)
    └── .htaccess
```

### 2. Set Up Python Application in cPanel

1. **Login to cPanel**

2. **Navigate to "Setup Python App"** (or "Python Selector")

3. **Create New Application:**
   - **Python Version:** 3.12 (or latest available)
   - **Application Root:** `magma7_proj` (or full path: `/home/username/magma7_proj`)
   - **Application URL:** Your domain (e.g., `magma7fitness.com`)
   - **Application Startup File:** `passenger_wsgi.py`
   - **Application Entry Point:** `application`

4. **Click "Create"**

5. **Note the Virtual Environment Path** shown (usually `/home/username/virtualenv/magma7_proj/3.12`)

### 3. Configure Environment Variables in cPanel

In the Python App configuration page, add these environment variables:

```
DJANGO_SETTINGS_MODULE=magma7.settings.production
DJANGO_SECRET_KEY=your-generated-secret-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
SITE_URL=https://yourdomain.com
```

### 4. Install Dependencies via SSH

SSH into your server and run:

```bash
# Navigate to project directory
cd ~/magma7_proj

# Activate the virtual environment (use the path from cPanel Python App)
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installations
pip list | grep -E "(Django|PyMySQL)"
```

### 5. Create MySQL Database in cPanel

1. **Go to "MySQL® Databases"** in cPanel

2. **Create a new database:**
   - Database name: `username_magmafit` (cPanel adds prefix)
   - Note the full database name shown

3. **Create a database user:**
   - Username: `username_magmadb`
   - Password: (generate strong password)

4. **Add user to database:**
   - Select the user and database
   - Grant "ALL PRIVILEGES"

5. **Update your `.env` file** with these database credentials

### 6. Update .env File

SSH into your server:

```bash
cd ~/magma7_proj
nano .env
```

Update with your actual values:

```env
DJANGO_SECRET_KEY=<generate-new-secret-key>
DJANGO_ALLOWED_HOSTS=magma7fitness.com,www.magma7fitness.com
DJANGO_SETTINGS_MODULE=magma7.settings.production

DB_NAME=username_magmafit
DB_USER=username_magmadb
DB_PASSWORD=<your-database-password>
DB_HOST=localhost
DB_PORT=3306

SITE_URL=https://magma7fitness.com
DEBUG=False
SECURE_SSL_REDIRECT=0
```

To generate a new SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 7. Run Django Migrations

```bash
cd ~/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set environment
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Create logs directory
mkdir -p logs

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 8. Configure public_html/.htaccess

**IMPORTANT:** Update the `.htaccess` file in `public_html/` with the correct username:

```bash
nano ~/public_html/.htaccess
```

**Replace `/home/username/` with your actual cPanel username:**

```apache
# Django Application Configuration for cPanel/Passenger
PassengerEnabled On
PassengerAppRoot /home/YOURUSERNAME/magma7_proj

# Allow access to public directory
Options +FollowSymLinks -Indexes

# Rest of your .htaccess content...
```

### 9. Set Up Static Files

Create symbolic link or copy static files to public_html:

```bash
# Option 1: Symbolic link (recommended)
ln -s ~/magma7_proj/staticfiles ~/public_html/static

# Option 2: Copy files
cp -r ~/magma7_proj/staticfiles ~/public_html/static

# Create media directory
mkdir -p ~/public_html/media
```

Update your `.htaccess` to serve static files:

```apache
# Serve static files directly
<IfModule mod_rewrite.c>
    RewriteEngine On

    # Serve static files
    RewriteCond %{REQUEST_URI} ^/static/ [NC]
    RewriteRule ^(.*)$ - [L]

    # Serve media files
    RewriteCond %{REQUEST_URI} ^/media/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

### 10. Restart the Application

**In cPanel:**
1. Go to "Setup Python App"
2. Find your application
3. Click the **"Restart"** button (or "Stop App" then "Start App")

**Or via command line:**
```bash
touch ~/magma7_proj/passenger_wsgi.py
# OR
touch ~/public_html/restart.txt
```

### 11. Test Your Application

Visit your domain: `https://yourdomain.com`

You should now see your Django application instead of the index.html file!

---

## Troubleshooting

### Still seeing index.html?

1. **Check passenger_wsgi.py exists** in your project root
2. **Verify .htaccess** has correct PassengerAppRoot path
3. **Check Python App is running** in cPanel (should show green status)
4. **Check error logs:**
   ```bash
   tail -f ~/logs/django_errors.log
   tail -f ~/passenger.log  # if exists
   ```

### Database connection errors?

```bash
# Test database connection
python manage.py dbshell
```

### Import errors?

```bash
# Verify all packages installed
source ~/virtualenv/magma7_proj/3.12/bin/activate
pip list
```

### Static files not loading?

1. Ensure `collectstatic` was run
2. Check STATIC_ROOT in settings
3. Verify symbolic link or files exist in public_html/static
4. Check file permissions: `chmod -R 755 ~/public_html/static`

### Check Application Logs

```bash
# Django error logs
tail -f ~/magma7_proj/logs/django_errors.log

# Passenger logs (if available)
tail -f ~/logs/passenger.log
```

### Force Restart Application

```bash
# Method 1: Touch WSGI file
touch ~/magma7_proj/passenger_wsgi.py

# Method 2: Create restart file
mkdir -p ~/public_html/tmp
touch ~/public_html/tmp/restart.txt

# Method 3: Via cPanel UI
# Go to Setup Python App → Click Restart
```

---

## Important Files Checklist

✅ `~/magma7_proj/passenger_wsgi.py` - Entry point for Passenger
✅ `~/magma7_proj/.env` - Environment variables
✅ `~/public_html/.htaccess` - Web server configuration
✅ `~/public_html/static/` - Collected static files
✅ Database created and configured in cPanel

---

## Post-Deployment

### Enable SSL (Recommended)

1. In cPanel, go to "SSL/TLS Status"
2. Enable AutoSSL for your domain
3. Wait for certificate to be issued
4. Update `.env`: `SECURE_SSL_REDIRECT=1`
5. Restart application

### Set up Cron Jobs (if needed)

For periodic tasks, add in cPanel Cron Jobs:
```bash
0 0 * * * cd ~/magma7_proj && source ~/virtualenv/magma7_proj/3.12/bin/activate && python manage.py your_command
```

### Monitor Application

- Check error logs regularly
- Set up uptime monitoring
- Monitor database size and performance

---

## Quick Reference Commands

```bash
# Activate virtual environment
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Restart Django app
touch ~/magma7_proj/passenger_wsgi.py

# View logs
tail -f ~/magma7_proj/logs/django_errors.log

# Django shell
cd ~/magma7_proj && python manage.py shell

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```
