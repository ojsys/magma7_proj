# Fix: Media Files Not Showing (404 Error)

## Problem

Uploaded media files (logos, images) return 404 error when accessed.

**Example error:**
```
Page not found (404)
Request URL: http://localhost:8000/media/branding/logo.png
```

## Root Cause

Django needs explicit configuration to serve media files during development and production.

---

## Solution Applied

### ✅ For Development (localhost)

**File updated:** `magma7/urls.py`

Added media file serving:
```python
from django.conf import settings
from django.conf.urls.static import static

# At the bottom of urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**This fix is already applied!** Just restart your development server:
```bash
# Stop your server (Ctrl+C)
# Then restart:
python manage.py runserver
```

Now visit the logo URL again - it should work!

---

## For Production (cPanel)

Production uses Apache/Passenger which serves media files differently.

### Option 1: Symlink (Recommended)

Create a symbolic link from `public_html/media` to `magma7_proj/media`:

```bash
ssh magmafit@yourserver
cd ~
ln -s /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

**Benefits:**
- No file duplication
- Changes instantly reflected
- Saves disk space

### Option 2: Copy Files

Copy media directory to public_html:

```bash
ssh magmafit@yourserver
cd ~
cp -r /home/magmafit/magma7_proj/media /home/magmafit/public_html/
```

**Note:** Need to recopy after each new upload.

### Option 3: Apache Alias (Already in .htaccess)

Your `.htaccess` should already have:
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_URI} ^/media/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

This tells Apache to serve media files directly.

---

## Deployment Script Updated

The `deploy_media_center.sh` script now automatically creates the symlink:

```bash
ssh magmafit@yourserver
./deploy_media_center.sh
```

It will:
1. Create media directories
2. Set correct permissions (755)
3. Create symlink: `public_html/media` → `magma7_proj/media`
4. Run migrations
5. Restart app

---

## Testing

### Local Development

1. **Restart Django server**:
   ```bash
   python manage.py runserver
   ```

2. **Upload a test image**:
   - Go to Admin → Media Assets
   - Upload an image
   - Click "File URL" to copy URL

3. **Test the URL**:
   - Paste URL in browser
   - Should show the image (not 404)
   - Example: `http://localhost:8000/media/media_assets/2025/01/test.jpg`

### Production (cPanel)

1. **After deployment**, test media URL:
   ```
   https://www.magma7fitness.com/media/branding/logo.png
   ```

2. **Should return the image**, not 404

3. **Check symlink exists**:
   ```bash
   ls -la ~/public_html/media
   # Should show: media -> /home/magmafit/magma7_proj/media
   ```

---

## Troubleshooting

### Still getting 404 on localhost?

**Restart the development server:**
```bash
# Press Ctrl+C to stop
python manage.py runserver
```

**Clear browser cache:**
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

**Check DEBUG is True:**
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
True  # Should be True for development
```

### Still getting 404 on production?

**Check symlink:**
```bash
ls -la ~/public_html/media
```

**If no symlink, create it:**
```bash
ln -s /home/magmafit/magma7_proj/media ~/public_html/media
```

**Check file permissions:**
```bash
ls -la /home/magmafit/magma7_proj/media/
# Directories should be 755
# Files should be 644

chmod 755 /home/magmafit/magma7_proj/media/
chmod 755 /home/magmafit/magma7_proj/media/branding/
chmod 644 /home/magmafit/magma7_proj/media/branding/*.png
```

**Check .htaccess has media rules:**
```bash
cat ~/public_html/.htaccess | grep media
```

Should show:
```apache
RewriteCond %{REQUEST_URI} ^/media/ [NC]
RewriteRule ^(.*)$ - [L]
```

**Restart application:**
```bash
touch ~/magma7_proj/passenger_wsgi.py
```

---

## Why This Happens

### Development
Django's development server (`runserver`) doesn't automatically serve media files for security reasons. You must explicitly configure it in `urls.py`.

### Production
Apache/Passenger needs to know where media files are located. Options:
1. **Symlink** - Point `public_html/media` to `magma7_proj/media`
2. **Alias** - Use `.htaccess` rewrite rules
3. **Copy** - Duplicate files to `public_html/media`

---

## Summary

**Fix applied for development:**
- ✅ Updated `magma7/urls.py` to serve media files in DEBUG mode
- 🔄 Restart your development server to apply

**Fix for production:**
- ✅ Deployment script creates symlink automatically
- 🔄 Run `deploy_media_center.sh` on server

**Test:**
- Upload a file in admin
- Click the file URL
- Should show the file, not 404

---

## Quick Commands

**Restart development server:**
```bash
python manage.py runserver
```

**Create symlink on production:**
```bash
ssh magmafit@yourserver
ln -s /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

**Check if it works:**
```bash
# Local
curl http://localhost:8000/media/branding/logo.png

# Production
curl https://www.magma7fitness.com/media/branding/logo.png
```

Both should return image data, not 404.
