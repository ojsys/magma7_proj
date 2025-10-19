# cPanel Deployment Instructions for Magma7 Fitness

## Summary of Changes Made

We've configured Django to use **PyMySQL** instead of MySQLdb for MySQL database connections.

### Files Modified:
1. `requirements.txt` - Added PyMySQL==1.1.1
2. `manage.py` - Added PyMySQL initialization
3. `magma7/wsgi.py` - Added PyMySQL initialization
4. `passenger_wsgi.py` - Added PyMySQL initialization

## Steps to Deploy on cPanel Server

### 1. Install PyMySQL on the Server

SSH into your cPanel server and run:

```bash
cd ~/magma7_proj
source virtualenv/bin/activate  # or the path to your venv
pip install PyMySQL==1.1.1
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### 2. Verify PyMySQL Installation

```bash
python -c "import pymysql; print(pymysql.VERSION)"
```

You should see the version number (e.g., (1, 1, 1, 'final', 0))

### 3. Set Environment Variables

Make sure your `.env` file on the server has these values set:

```bash
DJANGO_SECRET_KEY=<your-generated-secret-key>
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com,www.yourdomain.com
DJANGO_SETTINGS_MODULE=magma7.settings.production

# Database settings from cPanel
DB_NAME=magmafit_db
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>
DB_HOST=localhost
DB_PORT=3306
```

### 4. Run Migrations

```bash
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Restart the Application

In cPanel:
- Go to "Setup Python App"
- Click "Restart" button for your application

## Troubleshooting

### If you still get MySQLdb errors:

1. Make sure PyMySQL is installed in the correct virtual environment
2. Check that the PyMySQL initialization code is present in all WSGI files
3. Restart the Python application in cPanel

### Check PyMySQL is working:

```bash
python manage.py shell
>>> import pymysql
>>> pymysql.install_as_MySQLdb()
>>> import MySQLdb
>>> print("Success!")
```

### Test database connection:

```bash
python manage.py dbshell
```

This should connect you to your MySQL database.

## Notes

- PyMySQL is a pure-Python MySQL driver, so it's easier to install on cPanel
- It's fully compatible with Django's MySQL backend
- No system-level dependencies required (unlike mysqlclient)
