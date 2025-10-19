# 🚀 Magma7Fitness - Production Deployment Checklist

Use this checklist to ensure a smooth deployment to cPanel.

---

## Pre-Deployment (Do This First)

### 1. cPanel Setup
- [ ] Log in to cPanel account
- [ ] Create MySQL database
  - [ ] Database name: `username_magma7`
  - [ ] Database user created
  - [ ] User added to database with ALL PRIVILEGES
  - [ ] Note credentials (name, user, password, host)

- [ ] Set up Python application in cPanel
  - [ ] Python version 3.9 or higher selected
  - [ ] Application root set: `/home/username/magma7`
  - [ ] Application URL configured (your domain)

- [ ] Domain/SSL
  - [ ] Domain added to cPanel
  - [ ] SSL certificate installed (Let's Encrypt or custom)
  - [ ] HTTPS working

### 2. Payment Provider Setup
- [ ] Paystack account created
- [ ] Business verified (for live keys)
- [ ] LIVE API keys obtained (not test keys!)
  - [ ] Public key (pk_live_...)
  - [ ] Secret key (sk_live_...)

### 3. Email Setup
- [ ] Email account created or SMTP service configured
- [ ] App password generated (if using Gmail)
- [ ] Test email credentials

---

## File Preparation (Local Machine)

### 4. Update Configuration Files
- [ ] Update `passenger_wsgi.py`:
  ```python
  project_home = '/home/username/magma7'  # Your actual cPanel path
  VIRTUALENV = '/home/username/virtualenv/magma7/3.9/bin/activate_this.py'
  ```

- [ ] Update `magma7/settings.py`:
  - [ ] Comment out SQLite database
  - [ ] Uncomment MySQL database configuration

- [ ] Generate new Django SECRET_KEY:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

### 5. Create Production .env File
- [ ] Copy `.env.production.example` to `.env`
- [ ] Fill in all required values:
  - [ ] `DJANGO_SECRET_KEY` (generated above)
  - [ ] `DJANGO_DEBUG=0` ⚠️ **CRITICAL**
  - [ ] `DJANGO_ALLOWED_HOSTS` (your domain)
  - [ ] Database credentials
  - [ ] Email SMTP settings
  - [ ] Paystack LIVE keys ⚠️ **LIVE, not test!**
  - [ ] `SITE_URL=https://yourdomain.com`
  - [ ] `SECURE_SSL_REDIRECT=1`

### 6. Test Local Requirements
- [ ] All dependencies in `requirements.txt`
- [ ] `PyMySQL` added to requirements (for MySQL support)
- [ ] No syntax errors in code
- [ ] Migrations up to date

---

## File Upload

### 7. Upload to cPanel
Choose one method:

**Method A: SSH/SCP**
- [ ] Upload via rsync or scp:
  ```bash
  rsync -avz --exclude='venv' --exclude='*.pyc' --exclude='db.sqlite3' \
    ./ username@yourserver.com:/home/username/magma7/
  ```

**Method B: File Manager**
- [ ] Create zip file (exclude venv, *.pyc, db.sqlite3)
- [ ] Upload via cPanel File Manager
- [ ] Extract files in correct directory

### 8. Verify Upload
- [ ] SSH into server
- [ ] Navigate to application directory
- [ ] Verify all files present:
  - [ ] `passenger_wsgi.py`
  - [ ] `.htaccess`
  - [ ] `manage.py`
  - [ ] `requirements.txt`
  - [ ] `.env` file
  - [ ] All app directories

---

## Server Setup

### 9. Install Dependencies
```bash
cd /home/username/magma7
source virtualenv/bin/activate
pip install -r requirements.txt
# PyMySQL is already in requirements.txt
```

- [ ] Dependencies installed successfully
- [ ] No error messages
- [ ] Virtual environment activated
- [ ] PyMySQL installed (verify with: pip list | grep PyMySQL)

### 10. Configure .env Permissions
```bash
chmod 600 .env
```
- [ ] .env file secured (600 permissions)

### 11. Create Required Directories
```bash
mkdir -p media logs staticfiles backups
chmod 755 media logs staticfiles
```
- [ ] Directories created
- [ ] Permissions set correctly

---

## Database Setup

### 12. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
- [ ] No migration errors
- [ ] All tables created successfully

### 13. Create Superuser
```bash
python manage.py createsuperuser
```
- [ ] Admin account created
- [ ] Username and password noted securely

### 14. Create Initial Data
Log into Django shell and create membership plans:
```bash
python manage.py shell
```

```python
from memberships.models import Plan

Plan.objects.create(name='Monthly', price=25000, duration_days=30, is_active=True)
Plan.objects.create(name='Quarterly', price=65000, duration_days=90, is_active=True, is_featured=True)
Plan.objects.create(name='Annual', price=200000, duration_days=365, is_active=True)
```

- [ ] Membership plans created
- [ ] Plans visible in admin

---

## Static Files

### 15. Collect Static Files
```bash
python manage.py collectstatic --noinput
```
- [ ] Static files collected successfully
- [ ] No errors

### 16. Configure Static Files in cPanel
In cPanel Python App settings:
- [ ] Static URL: `/static/` → Path: `/home/username/magma7/staticfiles/`
- [ ] Static URL: `/media/` → Path: `/home/username/magma7/media/`

---

## Application Start

### 17. Restart Application
```bash
touch tmp/restart.txt
# Or use the deploy script:
./deploy.sh  # Select option 6
```
- [ ] Application restarted
- [ ] No error messages

---

## Testing

### 18. Basic Functionality Tests
- [ ] Visit homepage: `https://yourdomain.com`
- [ ] Homepage loads correctly
- [ ] No 500 errors
- [ ] Static files loading (CSS, images)

### 19. Admin Panel Tests
- [ ] Access admin: `https://yourdomain.com/admin`
- [ ] Login with superuser
- [ ] View plans, users, payments
- [ ] Admin styling correct

### 20. User Registration Tests
- [ ] Register new account
- [ ] Email verification (if enabled)
- [ ] Login successful
- [ ] Dashboard accessible

### 21. Payment Flow Tests

**IMPORTANT: Test with small amounts first!**

- [ ] View membership plans
- [ ] Select a plan
- [ ] Redirects to Paystack checkout
- [ ] Complete payment with test amount
- [ ] Redirected back to site
- [ ] Subscription activated
- [ ] Receipt email received
- [ ] Payment record in admin

### 22. Email Tests
- [ ] Password reset email works
- [ ] Payment receipt email received
- [ ] Notification emails working

---

## Security & Performance

### 23. Security Checks
- [ ] HTTPS enabled (green padlock in browser)
- [ ] `DEBUG=0` verified (no debug page on errors)
- [ ] `.env` file not accessible via browser
- [ ] Admin URL not `/admin` (optional but recommended)
- [ ] Strong passwords everywhere

### 24. Run Django Security Check
```bash
python manage.py check --deploy
```
- [ ] All security checks passed
- [ ] Warnings addressed (if any)

### 25. Performance Checks
- [ ] Page load times acceptable
- [ ] Static files loading quickly
- [ ] Database queries optimized

---

## Post-Deployment

### 26. Monitoring Setup
- [ ] Error logging working (`logs/django_errors.log`)
- [ ] Log rotation configured
- [ ] Monitoring/alerts set up (optional)

### 27. Backup Strategy
- [ ] Database backup configured
- [ ] Media files backup configured
- [ ] `.env` file backed up securely
- [ ] Backup schedule set (cron job)

Example backup cron job:
```bash
0 3 * * * cd /home/username/magma7 && ./deploy.sh backup
```

### 28. Cron Jobs (Optional)
Set up in cPanel Cron Jobs:

**Session cleanup (daily at 3 AM):**
```bash
0 3 * * * cd /home/username/magma7 && source virtualenv/bin/activate && python manage.py clearsessions
```

### 29. Documentation
- [ ] Production credentials stored securely
- [ ] Server access details documented
- [ ] Deployment date recorded
- [ ] Contact info for support updated

---

## Go Live!

### 30. Final Verification
- [ ] All checklist items completed
- [ ] All tests passed
- [ ] Team notified of deployment
- [ ] Support ready for issues

### 31. Announce Launch
- [ ] Update DNS (if needed)
- [ ] Social media announcement
- [ ] Email existing users
- [ ] Marketing materials ready

---

## Maintenance Reminders

### Regular Tasks
- **Daily**: Monitor error logs
- **Weekly**: Check payment transactions
- **Monthly**: Database backup verification
- **Quarterly**: Dependency updates
- **Annually**: SSL certificate renewal (if not auto-renewing)

### Update Process
When updating the application:
1. Backup database
2. Upload new code
3. Activate virtualenv
4. Install new dependencies
5. Run migrations
6. Collect static files
7. Restart application
8. Test thoroughly

---

## Emergency Contacts

**Hosting Support**: [Your cPanel hosting provider]
**Paystack Support**: support@paystack.com
**Django Community**: https://forum.djangoproject.com/

---

## Rollback Plan

If something goes wrong:

1. **Restore previous version**:
   ```bash
   git checkout previous-commit-hash  # If using git
   ```

2. **Restore database backup**:
   ```bash
   mysql -u username -p dbname < backup.sql
   ```

3. **Clear cache and restart**:
   ```bash
   python manage.py clearsessions
   touch tmp/restart.txt
   ```

---

**✅ Deployment Complete!**

Date Deployed: _______________
Deployed By: _______________
Version: _______________

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________
