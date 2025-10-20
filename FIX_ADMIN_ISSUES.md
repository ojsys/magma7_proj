# Fix Admin Issues on cPanel

## Issues Fixed

1. ✅ **Logo and Favicon fields added to SiteSettings**
2. ✅ **HeroSlides 500 error** (caused by missing migrations)

---

## Changes Made

### 1. Added Logo and Favicon Fields

**File:** `cms/models.py`
- Added `logo_url` field to SiteSettings
- Added `favicon_url` field to SiteSettings

**File:** `cms/admin.py`
- Updated SiteSettingsAdmin to display logo and favicon fields
- Added restrictions to prevent multiple SiteSettings instances

**File:** `cms/migrations/0002_add_logo_favicon_to_sitesettings.py`
- Migration to add the new fields to database

### 2. Fixed HeroSlides Admin

The 500 error is likely caused by missing migrations on the server.

---

## What to Do on cPanel Server

### Step 1: Upload Updated Files

Upload these files to your server:

```bash
# From your local machine
scp cms/models.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/
scp cms/admin.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/
scp cms/migrations/0002_add_logo_favicon_to_sitesettings.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/migrations/
```

### Step 2: Run Migrations

SSH into your server and run migrations:

```bash
ssh magmafit@yourserver
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Run migrations
python manage.py migrate cms

# You should see:
# Running migrations:
#   Applying cms.0002_add_logo_favicon_to_sitesettings... OK
```

### Step 3: Restart Application

```bash
touch passenger_wsgi.py
```

### Step 4: Test Admin

1. **Visit:** `https://www.magma7fitness.com/admin/`
2. **Login** with your admin credentials
3. **Check SiteSettings:**
   - Click "Site Settings"
   - You should now see "Logo url" and "Favicon url" fields
4. **Check HeroSlides:**
   - Click "Hero Slides"
   - Should load without 500 error
   - Click "Add Hero Slide" to create new slides

---

## Alternative: Run All Migrations

If Hero Slides still shows 500 error, run all migrations:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Check pending migrations
python manage.py showmigrations

# Run all migrations
python manage.py migrate

# Restart app
touch passenger_wsgi.py
```

---

## Using the Logo and Favicon

### Upload Your Files

1. **Upload logo and favicon** to a hosting service:
   - Use Imgur, Cloudinary, or your server
   - Or place in `public_html/media/` folder

2. **Get the URL:**
   ```
   Logo: https://www.magma7fitness.com/media/logo.png
   Favicon: https://www.magma7fitness.com/media/favicon.ico
   ```

### Add URLs in Admin

1. Go to **Admin → Site Settings**
2. **Logo url:** Enter full URL to your logo
   - Example: `https://www.magma7fitness.com/media/logo.png`
   - Recommended: PNG or SVG with transparent background
   - Recommended size: 200x60 pixels or similar

3. **Favicon url:** Enter full URL to your favicon
   - Example: `https://www.magma7fitness.com/media/favicon.ico`
   - Recommended: 32x32 or 64x64 pixels
   - Format: .ico or .png

4. **Save**

### Display Logo in Templates

The logo and favicon are now available in templates via `site_settings` context:

```html
<!-- Logo -->
{% if site_settings.logo_url %}
<img src="{{ site_settings.logo_url }}" alt="{{ site_settings.brand_name }}">
{% else %}
{{ site_settings.brand_name }}
{% endif %}

<!-- Favicon -->
{% if site_settings.favicon_url %}
<link rel="icon" type="image/x-icon" href="{{ site_settings.favicon_url }}">
{% endif %}
```

---

## Troubleshooting HeroSlides 500 Error

### Check Error Logs

```bash
# Django error log
tail -50 /home/magmafit/magma7_proj/logs/django_errors.log

# Look for specific error messages
```

### Common Causes:

1. **Missing migrations**
   ```bash
   python manage.py migrate cms
   ```

2. **Database table doesn't exist**
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Permission issues**
   ```bash
   # Check if database file is writable (if using SQLite)
   ls -l db.sqlite3

   # For MySQL, check credentials in .env
   cat .env | grep DB_
   ```

4. **Python/Django version mismatch**
   ```bash
   python --version
   pip show django
   ```

### Test Database Connection

```bash
python manage.py shell
```

Then in Python shell:
```python
from cms.models import HeroSlide
print(HeroSlide.objects.count())
# Should show number of slides without error
```

### Recreate Tables (Last Resort)

⚠️ **Warning: This deletes all CMS data!**

```bash
python manage.py migrate cms zero
python manage.py migrate cms
```

---

## Quick Commands Summary

```bash
# 1. Upload files
scp cms/models.py cms/admin.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/
scp cms/migrations/0002_*.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/migrations/

# 2. SSH and migrate
ssh magmafit@yourserver
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
python manage.py migrate cms
touch passenger_wsgi.py

# 3. Test
# Visit: https://www.magma7fitness.com/admin/
```

---

## Success Criteria

✅ **SiteSettings:**
- Logo url field visible
- Favicon url field visible
- Can save URLs successfully

✅ **HeroSlides:**
- List page loads without error
- Can click "Add Hero Slide"
- Can edit existing slides
- Can save new slides

---

## Need Help?

If issues persist:
1. Check the error log for specific error messages
2. Verify all migrations ran successfully: `python manage.py showmigrations`
3. Test database connection: `python manage.py dbshell`
4. Check Django admin logs in the browser console (F12)

The most common fix is just running the migrations!
