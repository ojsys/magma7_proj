# Fixing Static Files (CSS, JS, Images)

## Issue
Your Django app is working but styles (CSS), JavaScript, and images are not loading.

---

## Solution: 3 Steps

### Step 1: Collect Static Files

SSH into your server and run:

```bash
cd /home/magmafit/magma7_proj

# Activate virtual environment
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Collect all static files
python manage.py collectstatic --noinput
```

This will copy all CSS, JS, and images from your Django apps into the `staticfiles` directory.

You should see output like:
```
120 static files copied to '/home/magmafit/magma7_proj/staticfiles'.
```

---

### Step 2: Create Symbolic Link to public_html

Django serves static files from `staticfiles/`, but Apache serves from `public_html/`. Create a link:

```bash
# Create static directory link
ln -s /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static

# Create media directory link (for user uploads)
mkdir -p /home/magmafit/magma7_proj/media
ln -s /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

**Alternative (if symbolic links don't work):**
Copy the files instead:
```bash
cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
cp -r /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

---

### Step 3: Configure Static Files in cPanel Python App

1. **Go to cPanel → Setup Python App**
2. **Find your application** and click **"Edit"**
3. **Scroll down to "Static files"** section
4. **Add static file mappings:**

   **URL:** `/static/`
   **Path:** `/home/magmafit/public_html/static`

   **URL:** `/media/`
   **Path:** `/home/magmafit/public_html/media`

5. **Click "Save"**
6. **Restart** the application

---

## Verification

### Check if static files exist:

```bash
# List static files
ls -la /home/magmafit/magma7_proj/staticfiles/

# Check public_html link
ls -la /home/magmafit/public_html/static/

# Check if CSS files exist
ls -la /home/magmafit/public_html/static/css/
ls -la /home/magmafit/public_html/static/admin/css/
```

### Test static file access directly:

Visit these URLs in your browser:
- `https://www.magma7fitness.com/static/admin/css/base.css`
- `https://www.magma7fitness.com/static/css/style.css` (if you have custom CSS)

If you get a 404, static files aren't being served correctly.

---

## Troubleshooting

### Static Files Still Not Loading?

#### Check 1: Verify .htaccess allows static files

Your `.htaccess` in `public_html/` should have these rules (already configured):

```apache
<IfModule mod_rewrite.c>
    RewriteEngine On

    # Serve static files directly (don't route through Django)
    RewriteCond %{REQUEST_URI} ^/static/ [NC]
    RewriteRule ^(.*)$ - [L]

    # Serve media files directly (don't route through Django)
    RewriteCond %{REQUEST_URI} ^/media/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

#### Check 2: Verify file permissions

```bash
chmod 755 /home/magmafit/public_html/static
chmod -R 644 /home/magmafit/public_html/static/*
find /home/magmafit/public_html/static -type d -exec chmod 755 {} \;
```

#### Check 3: Check browser console for errors

1. Open your website
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Look for 404 errors on static files
5. Check what URL it's trying to load

#### Check 4: Verify Django settings

SSH and check:
```bash
cd /home/magmafit/magma7_proj
python manage.py shell
```

In Python shell:
```python
from django.conf import settings
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
```

Should show:
```
STATIC_URL: /static/
STATIC_ROOT: /home/magmafit/magma7_proj/staticfiles
STATICFILES_DIRS: ['/home/magmafit/magma7_proj/static']
```

---

## Common Issues & Solutions

### Issue 1: 404 on /static/admin/css/base.css

Django admin static files not collected.

**Fix:**
```bash
python manage.py collectstatic --noinput --clear
```

### Issue 2: Symbolic link not working

Some cPanel setups don't allow symlinks.

**Fix:** Copy files instead
```bash
rm /home/magmafit/public_html/static  # Remove symlink
cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
```

**Note:** You'll need to copy files again after running collectstatic.

### Issue 3: Files exist but still 404

.htaccess might be blocking access.

**Fix:** Check .htaccess doesn't have these lines:
```apache
# REMOVE OR COMMENT THESE IF PRESENT:
# <FilesMatch "\.(css|js)$">
#     Require all denied
# </FilesMatch>
```

### Issue 4: Static files work but custom CSS doesn't

Your custom CSS might not be in the right location.

**Check:**
```bash
ls -la /home/magmafit/magma7_proj/static/css/
```

If custom CSS files are here, they should be collected. If not, create the directory:
```bash
mkdir -p /home/magmafit/magma7_proj/static/css/
# Add your CSS files here
python manage.py collectstatic --noinput
```

---

## Production Workflow

Every time you update static files:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# If using copy method (not symlink):
cp -r staticfiles/* /home/magmafit/public_html/static/

# Restart app
touch passenger_wsgi.py
```

---

## Alternative: WhiteNoise (Advanced)

For easier static file handling, you can use WhiteNoise:

```bash
pip install whitenoise
```

Add to `magma7/settings/base.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Optional: Enable compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

With WhiteNoise, Django serves static files itself (no need for symlinks or cPanel configuration).

---

## Quick Reference

```bash
# Collect static files
python manage.py collectstatic --noinput

# Create symlink (method 1)
ln -s /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static

# Copy files (method 2)
cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static

# Test static file
curl https://www.magma7fitness.com/static/admin/css/base.css

# Check permissions
ls -la /home/magmafit/public_html/static/

# View page source
# Look for: <link rel="stylesheet" href="/static/...">
```

---

## Success Criteria

✅ Your site is fully working when:
- Homepage loads with proper styling
- Admin panel looks correct (has CSS)
- Images load properly
- JavaScript works
- No 404 errors in browser console

Need more help? Check browser console (F12) for specific error messages!
