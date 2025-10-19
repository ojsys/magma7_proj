# Fixing 403 Forbidden Error - Django on cPanel

## Current Situation

You're getting a **403 Forbidden** error when accessing `www.magma7fitness.com` after removing the `index.html` file. This means Apache/Passenger is not properly routing requests to your Django application.

---

## ✅ Step-by-Step Fix

### Step 1: Verify Python App Configuration in cPanel

1. **Log into cPanel**

2. **Go to "Setup Python App"** (or "Python Selector")

3. **Check if your application exists:**
   - If NO app exists → Create one (see Step 2)
   - If app exists → Verify settings (see Step 3)

### Step 2: Create Python Application (If Not Exists)

Click **"Create Application"** and configure:

```
Python version: 3.12
Application root: magma7_proj
Application URL: (leave empty for root domain or select your domain)
Application startup file: passenger_wsgi.py
Application Entry point: application
```

**IMPORTANT:**
- Application root should be `magma7_proj` (NOT `public_html`)
- This is the directory where `manage.py` and `passenger_wsgi.py` are located

Click **"Create"** and wait for the app to be set up.

### Step 3: Verify Application Settings

If the app already exists, click **"Edit"** and verify:

**Application Settings:**
```
Application root: /home/magmafit/magma7_proj
Application URL: your domain
Application startup file: passenger_wsgi.py
Application Entry point: application
```

**Configuration files:**
```
Passenger log file: (auto-generated)
```

### Step 4: Add Environment Variables (Optional but Recommended)

In the Python App configuration page, scroll down to **"Environment variables"** and add:

```
DJANGO_SETTINGS_MODULE = magma7.settings.production
```

Click **"Save"**

### Step 5: Update .htaccess in public_html

The `.htaccess` file has been updated with the correct configuration. Upload it to your server:

**Location:** `/home/magmafit/public_html/.htaccess`

**Key directives:**
```apache
PassengerEnabled On
PassengerAppRoot /home/magmafit/magma7_proj
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/magmafit/virtualenv/magma7_proj/3.12/bin/python
```

### Step 6: Verify Directory Structure on Server

SSH into your server and verify:

```bash
# Check project directory
ls -la /home/magmafit/magma7_proj/

# Should show:
# - passenger_wsgi.py
# - manage.py
# - magma7/ (directory)
# - core/, memberships/, etc.
# - requirements.txt
# - .env

# Check public_html
ls -la /home/magmafit/public_html/

# Should show:
# - .htaccess
# - static/ (optional - for static files)
# - media/ (optional - for uploads)
```

### Step 7: Check File Permissions

```bash
# Ensure proper permissions
chmod 755 /home/magmafit/magma7_proj
chmod 644 /home/magmafit/magma7_proj/passenger_wsgi.py
chmod 644 /home/magmafit/public_html/.htaccess

# Make sure passenger_wsgi.py is readable
chmod +r /home/magmafit/magma7_proj/passenger_wsgi.py
```

### Step 8: Verify passenger_wsgi.py

Check the contents of `passenger_wsgi.py`:

```bash
cat /home/magmafit/magma7_proj/passenger_wsgi.py
```

It should have:
```python
import pymysql
pymysql.install_as_MySQLdb()

# ... path configuration ...

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 9: Restart the Application

**Method 1: Via cPanel**
1. Go to "Setup Python App"
2. Find your app
3. Click **"Restart"** or **"Stop App"** then **"Start App"**

**Method 2: Via SSH**
```bash
# Touch the WSGI file to trigger restart
touch /home/magmafit/magma7_proj/passenger_wsgi.py

# Or create a restart file
mkdir -p /home/magmafit/public_html/tmp
touch /home/magmafit/public_html/tmp/restart.txt
```

### Step 10: Check Application Logs

```bash
# Check Django error logs
tail -f /home/magmafit/magma7_proj/logs/django_errors.log

# Check Passenger logs (if available)
tail -f /home/magmafit/logs/passenger.log

# Check Apache error logs (in cPanel)
# Go to: Metrics → Errors
```

---

## 🔍 Troubleshooting

### Issue 1: Still Getting 403 Error

**Possible Causes:**
1. Python app not created in cPanel
2. Wrong paths in .htaccess
3. Passenger not enabled

**Fix:**
```bash
# Verify Passenger is running
ps aux | grep -i passenger

# Check .htaccess syntax
cd /home/magmafit/public_html
cat .htaccess
```

### Issue 2: "Internal Server Error" (500)

This means Django app has an error. Check logs:

```bash
tail -50 /home/magmafit/magma7_proj/logs/django_errors.log
```

Common causes:
- Missing environment variables in .env
- Database connection error
- Missing dependencies

### Issue 3: Static Files Not Loading

Django app works but CSS/JS/images don't load:

```bash
# Collect static files
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
python manage.py collectstatic --noinput

# Create symbolic link
ln -s /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static

# Or copy files
cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
```

### Issue 4: "Module Not Found" Errors

Missing dependencies:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
pip install -r requirements.txt

# Verify installations
pip list | grep -E "(Django|PyMySQL)"
```

### Issue 5: Database Connection Errors

Check .env file:

```bash
cat /home/magmafit/magma7_proj/.env
```

Verify database credentials:
```bash
mysql -u your_db_user -p -h localhost your_db_name
```

---

## 📋 Quick Checklist

Before you proceed, verify:

- [ ] Python app created in cPanel "Setup Python App"
- [ ] Application root points to `/home/magmafit/magma7_proj`
- [ ] `passenger_wsgi.py` exists in project root
- [ ] `.htaccess` uploaded to `/home/magmafit/public_html/`
- [ ] Correct paths in .htaccess (username = `magmafit`)
- [ ] Virtual environment activated when installing packages
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] .env file configured with correct values
- [ ] Application restarted after changes

---

## 🚀 Testing

After completing all steps:

1. **Visit your domain:** `https://www.magma7fitness.com`
   - Should see Django app (not 403)

2. **Check admin:** `https://www.magma7fitness.com/admin`
   - Should see Django admin login

3. **Check static files:** View page source and check if CSS loads

4. **Monitor logs:**
   ```bash
   tail -f /home/magmafit/magma7_proj/logs/django_errors.log
   ```

---

## 📞 Need More Help?

If you're still getting 403:

1. **Check cPanel error logs** (Metrics → Errors)
2. **Contact your hosting provider** - They can check:
   - If Passenger is enabled for your account
   - If mod_passenger is loaded
   - Server-level restrictions

3. **Share error logs** for specific troubleshooting

---

## Alternative: Using Subdirectory

If you can't get it working in root, try deploying to a subdirectory:

**In cPanel Python App:**
- Application URL: `/app` (or any path)

**Visit:** `https://www.magma7fitness.com/app`

This is easier to configure but your site won't be at the root domain.

---

## ✅ Success Criteria

Your Django app is working when:

✅ Visiting your domain shows Django content (not 403)
✅ Admin panel accessible at `/admin`
✅ Static files (CSS, JS, images) loading
✅ No errors in Django logs
✅ Database queries working
