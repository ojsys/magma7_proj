# Database Configuration - PyMySQL

## Overview

This Django project uses **PyMySQL** as the MySQL database driver instead of mysqlclient.

### Why PyMySQL?

- ✅ **Pure Python** - No system-level dependencies required
- ✅ **Easy to install** - Works on cPanel without sudo access
- ✅ **Fully compatible** - Drop-in replacement for MySQLdb
- ✅ **No compilation** - No need for MySQL development headers

### What's Configured

The following files have been configured to use PyMySQL:

1. **requirements.txt** - Includes `PyMySQL==1.1.1`
2. **manage.py** - Initializes PyMySQL before Django starts
3. **magma7/wsgi.py** - Initializes PyMySQL for production WSGI
4. **passenger_wsgi.py** - Initializes PyMySQL for cPanel Passenger

### Installation

Simply install from requirements.txt:

```bash
pip install -r requirements.txt
```

This will install PyMySQL along with all other dependencies.

### Verification

To verify PyMySQL is installed and working:

```bash
# Check if PyMySQL is installed
pip list | grep PyMySQL

# Test PyMySQL initialization
python -c "import pymysql; pymysql.install_as_MySQLdb(); import MySQLdb; print('✅ PyMySQL working!')"

# Test database connection
python manage.py check --database default
```

### Database Settings

Your production settings (`magma7/settings/production.py`) are configured to use MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Django's MySQL backend
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

PyMySQL automatically acts as the MySQLdb driver for this configuration.

### Environment Variables

Make sure your `.env` file includes these database settings:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
```

### Troubleshooting

#### "No module named 'MySQLdb'"

This means PyMySQL isn't installed or not initialized. Fix:

```bash
# Install PyMySQL
pip install PyMySQL

# Verify it's in requirements.txt
grep PyMySQL requirements.txt
```

#### "Access denied for user"

Database credentials are incorrect. Check:

1. Database name, user, and password in `.env`
2. Database user has privileges on the database
3. Database host is correct (usually `localhost` on cPanel)

#### "Can't connect to MySQL server"

MySQL server isn't running or host is wrong:

```bash
# Test MySQL connection
mysql -u your_user -p -h localhost your_database
```

### cPanel MySQL Database Setup

1. **Create Database** in cPanel → MySQL Databases
   - Name: `username_magmafit` (cPanel adds prefix)

2. **Create User**
   - Username: `username_magmadb`
   - Strong password

3. **Add User to Database**
   - Grant ALL PRIVILEGES

4. **Update .env** with these credentials

### Migration Commands

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# View SQL for a migration (optional)
python manage.py sqlmigrate app_name 0001
```

### Database Backup

Create regular backups of your database:

```bash
# Export database
mysqldump -u username -p database_name > backup_$(date +%Y%m%d).sql

# Import database
mysql -u username -p database_name < backup_20250120.sql
```

### Performance Tips

1. **Connection Pooling** - Already configured with `CONN_MAX_AGE = 600`
2. **Indexes** - Make sure your models have appropriate indexes
3. **Query Optimization** - Use `select_related()` and `prefetch_related()`

### Support

- **PyMySQL Docs**: https://pymysql.readthedocs.io/
- **Django MySQL**: https://docs.djangoproject.com/en/stable/ref/databases/#mysql-notes
- **cPanel MySQL**: Contact your hosting provider

---

## Quick Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Check PyMySQL
pip show PyMySQL

# Test database
python manage.py dbshell

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

✅ **No mysqlclient or system dependencies required!**
