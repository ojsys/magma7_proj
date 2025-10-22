# Deploy Home Gallery to Production - Quick Guide

## The Error

```
django.db.utils.ProgrammingError: (1146, "Table 'magmafit_db.cms_homegalleryimage' doesn't exist")
```

**Cause:** The HomeGalleryImage table hasn't been created in production yet.

**Fix:** Run the migration!

---

## Quick Fix (5 Minutes)

### Step 1: Upload Files to cPanel

Use **cPanel File Manager** to upload these files:

**Navigate to:** `/home/magmafit/magma7_proj/`

**Upload these files:**

1. **`cms/models.py`** → `/home/magmafit/magma7_proj/cms/`
2. **`cms/admin.py`** → `/home/magmafit/magma7_proj/cms/`
3. **`core/views.py`** → `/home/magmafit/magma7_proj/core/`
4. **`core/templates/core/home.html`** → `/home/magmafit/magma7_proj/core/templates/core/`
5. **`static/css/styles.css`** → `/home/magmafit/magma7_proj/static/css/`
6. **`cms/migrations/0009_homegalleryimage.py`** → `/home/magmafit/magma7_proj/cms/migrations/`

### Step 2: Run Migration

Open **cPanel Terminal** and run:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Run the migration
python manage.py migrate cms

# Collect static files
python manage.py collectstatic --noinput

# Restart application
touch passenger_wsgi.py
```

### Step 3: Test

Visit: https://www.magma7fitness.com/

**✓ The error should be gone!**

The homepage will load, but the gallery section won't show yet (no images added).

---

## Alternative: Use Deployment Script

### Upload and run the script:

1. Upload `deploy_home_gallery.sh` to `/home/magmafit/magma7_proj/`
2. Upload all the files listed above
3. Run in cPanel Terminal:

```bash
cd /home/magmafit/magma7_proj
bash deploy_home_gallery.sh
```

---

## After Deployment

### Add Gallery Images

1. Go to: https://www.magma7fitness.com/admin/cms/homegalleryimage/
2. Click **"Add Home Gallery Image"**
3. Fill in:
   - **Image URL:** From Media Center or external URL
   - **Title:** e.g., "Main Gym Floor"
   - **Description:** Brief description (optional)
   - **Order:** 0, 1, 2, 3... (lower first)
   - **Is active:** Check ✓
4. Save

Add 6-8 images for best results.

### Verify on Homepage

Visit: https://www.magma7fitness.com/

Scroll down - you should see the **"Our State-of-the-Art Facility"** section with your gallery!

---

## Files to Upload - Detailed

### 1. cms/models.py
**Location:** `/home/magmafit/magma7_proj/cms/models.py`
**Purpose:** Contains HomeGalleryImage model definition

### 2. cms/admin.py
**Location:** `/home/magmafit/magma7_proj/cms/admin.py`
**Purpose:** Admin interface for managing gallery

### 3. core/views.py
**Location:** `/home/magmafit/magma7_proj/core/views.py`
**Purpose:** Passes gallery images to homepage template

### 4. core/templates/core/home.html
**Location:** `/home/magmafit/magma7_proj/core/templates/core/home.html`
**Purpose:** Displays gallery section on homepage

### 5. static/css/styles.css
**Location:** `/home/magmafit/magma7_proj/static/css/styles.css`
**Purpose:** Gallery styling and animations

### 6. cms/migrations/0009_homegalleryimage.py
**Location:** `/home/magmafit/magma7_proj/cms/migrations/0009_homegalleryimage.py`
**Purpose:** Creates the database table

---

## Migration Commands Explained

```bash
# Show current migration status
python manage.py showmigrations cms

# Run migrations (creates the table)
python manage.py migrate cms

# Verify table was created
python manage.py dbshell
```

Then in MySQL:
```sql
SHOW TABLES LIKE 'cms_homegalleryimage';
DESCRIBE cms_homegalleryimage;
exit;
```

---

## Troubleshooting

### "Migration already applied"

This is good! The table already exists. Just restart:
```bash
touch passenger_wsgi.py
```

### "No such file or directory: 0009_homegalleryimage.py"

Make sure you uploaded the migration file to:
`/home/magmafit/magma7_proj/cms/migrations/0009_homegalleryimage.py`

### Homepage still shows error

1. Check you restarted: `touch passenger_wsgi.py`
2. Check migration ran: `python manage.py migrate cms`
3. Check table exists: `python manage.py dbshell` then `SHOW TABLES;`

### Gallery section not showing

This is normal! The section only shows if you have gallery images.

Add images at: `/admin/cms/homegalleryimage/`

---

## Quick Deployment Checklist

- [ ] Upload `cms/models.py`
- [ ] Upload `cms/admin.py`
- [ ] Upload `core/views.py`
- [ ] Upload `core/templates/core/home.html`
- [ ] Upload `static/css/styles.css`
- [ ] Upload `cms/migrations/0009_homegalleryimage.py`
- [ ] Run: `python manage.py migrate cms`
- [ ] Run: `python manage.py collectstatic --noinput`
- [ ] Run: `touch passenger_wsgi.py`
- [ ] Test homepage: https://www.magma7fitness.com/
- [ ] Add gallery images in admin
- [ ] Verify gallery appears on homepage

---

## Expected Migration Output

```
Operations to perform:
  Apply all migrations: cms
Running migrations:
  Applying cms.0009_homegalleryimage... OK
```

If you see this ✓ you're done!

---

## Summary

**Problem:** Table doesn't exist
**Solution:** Run migration to create it
**Time:** 5 minutes
**Commands:**
```bash
python manage.py migrate cms
python manage.py collectstatic --noinput
touch passenger_wsgi.py
```

**Status:** Ready to deploy ✓
