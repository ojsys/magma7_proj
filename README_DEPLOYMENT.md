# Magma7Fitness - Quick Deployment Reference

## 📁 Deployment Files Overview

Your project is now ready for cPanel deployment with the following files:

### Core Deployment Files

1. **`passenger_wsgi.py`** - WSGI entry point for cPanel's Passenger server
2. **`.htaccess`** - URL rewriting and security rules
3. **`requirements.txt`** - Python dependencies list
4. **`.env.production.example`** - Production environment template
5. **`deploy.sh`** - Interactive deployment automation script
6. **`DEPLOYMENT_GUIDE.md`** - Complete step-by-step deployment guide

### Configuration Updates

- **`magma7/settings.py`** - Updated with production-ready settings including:
  - MySQL database configuration (commented out, ready to activate)
  - Security headers for production
  - Logging configuration
  - HTTPS/SSL settings

---

## 🚀 Quick Start Deployment

### 1. Upload Files to cPanel

```bash
# Option A: Using rsync (recommended)
rsync -avz --exclude='venv' --exclude='*.pyc' --exclude='db.sqlite3' \
  ./ username@yourserver.com:/home/username/magma7/

# Option B: Create a zip and upload via cPanel File Manager
zip -r magma7.zip . -x "venv/*" "*.pyc" "db.sqlite3" "*.log"
```

### 2. Configure Environment

SSH into your server:
```bash
ssh username@yourserver.com
cd /home/username/magma7
```

Create your `.env` file from the template:
```bash
cp .env.production.example .env
nano .env  # Edit with your actual credentials
chmod 600 .env  # Secure the file
```

### 3. Run Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

Then select option **5** (Run All) to:
- Install dependencies
- Run migrations
- Collect static files

### 4. Create Superuser

In the deploy script menu, select option **4** to create an admin account.

### 5. Restart Application

Select option **6** in the deploy script to restart the application.

---

## ✅ Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] Created MySQL database in cPanel
- [ ] Updated `passenger_wsgi.py` with correct paths
- [ ] Created `.env` file with production credentials
- [ ] Set `DJANGO_DEBUG=0` in `.env`
- [ ] Generated unique `DJANGO_SECRET_KEY`
- [ ] Updated `ALLOWED_HOSTS` with your domain
- [ ] Using LIVE payment keys (not test keys)
- [ ] Configured email SMTP settings
- [ ] Installed SSL certificate
- [ ] Created Python app in cPanel

---

## 📚 Important Files Explained

### `passenger_wsgi.py`
The entry point for Passenger (cPanel's WSGI server). Update these lines:
```python
project_home = '/home/username/magma7'  # Your actual path
VIRTUALENV = '/home/username/virtualenv/magma7/3.9/bin/activate_this.py'
```

### `.htaccess`
Handles URL rewriting and serves static files. Protects sensitive files like `.env`.

### `deploy.sh`
Interactive menu script with options:
1. Install Dependencies
2. Run Migrations
3. Collect Static Files
4. Create Superuser
5. Run All (1-3)
6. Restart Application
7. Check Status
8. View Error Logs
9. Backup Database

### `.env` (Production)
Critical environment variables:
- Database credentials
- Secret key
- Payment API keys
- Email settings
- Domain configuration

**⚠️ NEVER commit this file to git!**

---

## 🔧 Common Tasks

### Update Application
```bash
cd /home/username/magma7
source virtualenv/bin/activate
git pull origin main  # If using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

### View Logs
```bash
tail -f logs/django_errors.log
```

### Database Backup
```bash
./deploy.sh  # Then select option 9
# Or manually:
mysqldump -u dbuser -p dbname > backup.sql
```

### Test Configuration
```bash
python manage.py check --deploy
```

---

## 🐛 Troubleshooting

### 500 Internal Server Error
1. Check `logs/django_errors.log`
2. Verify `.env` file exists and is readable
3. Ensure `DEBUG=0` in production
4. Check database credentials

### Static Files Not Loading
1. Run: `python manage.py collectstatic`
2. Verify static file mapping in cPanel Python App settings
3. Check file permissions (755 for dirs, 644 for files)

### Database Connection Error
1. Verify credentials in `.env`
2. Test: `python manage.py dbshell`
3. Check MySQL user permissions

### Import Errors
1. Activate virtualenv: `source virtualenv/bin/activate`
2. Reinstall: `pip install -r requirements.txt`

---

## 📞 Support Resources

- **Full Guide**: See `DEPLOYMENT_GUIDE.md` for detailed instructions
- **Django Docs**: https://docs.djangoproject.com/
- **cPanel Docs**: https://docs.cpanel.net/
- **Passenger Docs**: https://www.phusionpassenger.com/docs/

---

## 🔐 Security Reminders

1. **Always use HTTPS** in production
2. **Never commit `.env`** to version control
3. **Use strong passwords** for database and admin
4. **Keep Django updated** for security patches
5. **Use LIVE payment keys** in production
6. **Regular backups** of database and media files
7. **Monitor error logs** regularly

---

## 📝 Next Steps After Deployment

1. Test the website thoroughly
2. Create membership plans in admin
3. Test payment flow with small amount
4. Configure automated backups
5. Set up monitoring/alerts
6. Test email receipts
7. Verify SSL certificate
8. Add domain to Google Search Console
9. Set up cron jobs for maintenance

---

**Ready to deploy? Start with the `DEPLOYMENT_GUIDE.md` for detailed instructions!**
