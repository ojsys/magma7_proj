# Fix Yellow Overlay on Pricing Cards (cPanel)

## Problem
The pricing cards on the membership page are covered with a yellow (gold) overlay on the cPanel host, making text unreadable. Works fine locally.

## Cause
This is likely because:
1. Old CSS cached on the server
2. Static files not collected after recent changes
3. The `.featured` class has aggressive gold background styling

---

## Solution 1: Collect Static Files (Most Likely Fix)

SSH into your server and run:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Collect static files (overwrites old CSS)
python manage.py collectstatic --noinput --clear

# If using symlink
# Static files will be automatically available

# If using copy method
cp -r staticfiles/* /home/magmafit/public_html/static/

# Restart app
touch passenger_wsgi.py
```

---

## Solution 2: Clear Browser Cache

After collecting static files:

1. **Hard refresh your browser:**
   - Chrome/Edge: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
   - Firefox: `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)

2. **Or clear cache completely:**
   - Chrome: Settings → Privacy → Clear browsing data → Cached images and files

3. **Test in incognito/private window:**
   - This ensures fresh CSS is loaded

---

## Solution 3: Check CSS File Version

Verify the CSS file is updated on server:

```bash
# Check when CSS was last modified
ls -lh /home/magmafit/public_html/static/css/

# View the CSS content
cat /home/magmafit/public_html/static/css/style.css | grep featured

# Or check in Django staticfiles
ls -lh /home/magmafit/magma7_proj/staticfiles/css/
```

---

## Solution 4: Add Cache-Busting

If the issue persists, add version parameter to CSS links.

Edit `base.html` or the pricing template:

```html
<!-- Instead of: -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- Use: -->
<link rel="stylesheet" href="{% static 'css/style.css' %}?v={{ VERSION }}">

<!-- Or with timestamp: -->
<link rel="stylesheet" href="{% static 'css/style.css' %}?v=20251020">
```

---

## Solution 5: Override Featured Card Styles

If static files are collected but issue persists, add inline override in the template.

Add this style block to `memberships/templates/memberships/plans.html`:

```html
<style>
/* Fix for featured card overlay */
.card.featured {
    background: var(--card-bg) !important;
}

.card.featured .card-content {
    background: transparent !important;
}

.card.featured::before,
.card.featured::after {
    display: none !important;
}

/* Ensure text is visible */
.card h4,
.card .card-title,
.card span,
.card p {
    color: var(--text-primary) !important;
    position: relative !important;
    z-index: 10 !important;
}

.card .price {
    color: var(--primary-green) !important;
}
</style>
```

---

## Quick Test Commands

```bash
# 1. SSH to server
ssh magmafit@yourserver

# 2. Navigate to project
cd /home/magmafit/magma7_proj

# 3. Activate venv
source ~/virtualenv/magma7_proj/3.12/bin/activate

# 4. Collect static files
python manage.py collectstatic --noinput --clear

# 5. Check files were updated
ls -lh staticfiles/css/

# 6. Restart app
touch passenger_wsgi.py

# 7. Clear browser cache and test
```

---

## Verify It's Fixed

1. **Visit:** `https://www.magma7fitness.com/memberships/plans/`
2. **Check pricing cards are readable**
3. **Verify all text is visible:**
   - Plan name
   - Price
   - Features list
   - Buttons

---

## If Still Not Working

### Check Static URL in Production Settings

Verify `magma7/settings/production.py` has:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Check .htaccess Allows Static Files

Verify `/home/magmafit/public_html/.htaccess` has:

```apache
<IfModule mod_rewrite.c>
    RewriteEngine On

    # Serve static files directly
    RewriteCond %{REQUEST_URI} ^/static/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

### View Source in Browser

1. Right-click on page → View Source
2. Find CSS link: `<link rel="stylesheet" href="/static/css/style.css">`
3. Click the link to view CSS file
4. Search for `.featured` class
5. Check what styles are applied

### Browser DevTools Inspection

1. Press `F12` to open DevTools
2. Click on a yellow card
3. Go to "Elements" tab
4. Look at "Styles" panel on right
5. See what CSS rules are being applied
6. Note any `background` or `::before` pseudo-elements

---

## Most Likely Solution

**90% of the time, this is fixed by:**

```bash
python manage.py collectstatic --noinput --clear
touch passenger_wsgi.py
# Then hard refresh browser (Ctrl+Shift+R)
```

---

## Prevention

To avoid this in future:

1. **Always collect static files after CSS changes:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Add to deployment script:**
   ```bash
   #!/bin/bash
   cd /home/magmafit/magma7_proj
   source ~/virtualenv/magma7_proj/3.12/bin/activate
   git pull
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput --clear
   touch passenger_wsgi.py
   ```

3. **Use cache-busting for CSS:**
   ```python
   # In settings
   STATIC_VERSION = '1.0.1'

   # In template
   ?v={{ settings.STATIC_VERSION }}
   ```

---

## Summary

✅ **Do this first:** Collect static files and restart app
✅ **Then:** Hard refresh browser (Ctrl+Shift+R)
✅ **If needed:** Add inline CSS override
✅ **Verify:** Check in incognito window

The issue is CSS caching - new styles exist locally but old styles are cached on the server!
