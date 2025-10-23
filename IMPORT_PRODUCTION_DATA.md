# Import Production Data to Local SQLite

## Quick Start (Use the Script!)

```bash
# 1. Make sure production_data.json is in project root
# 2. Run the safe import script:
bash import_production_safe.sh
```

**Default admin login after import:**
- Username: `admin`
- Password: `admin123`

---

## Manual Method (If You Prefer)

The easiest way to import production data is to use Django's management commands on the production server, then load locally.

### Step 1: Export Data from Production (cPanel)

Run this on your cPanel Terminal:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Export data to JSON
python manage.py dumpdata \
  cms.sitesettings \
  cms.heroslide \
  cms.program \
  cms.service \
  cms.partner \
  cms.testimonial \
  cms.mediaasset \
  cms.homegalleryimage \
  cms.aboutpage \
  cms.corevalue \
  cms.whychooseusitem \
  cms.aboutgalleryimage \
  cms.aboutstatistic \
  cms.facility \
  cms.teammember \
  cms.facilitiespage \
  cms.teampage \
  memberships.plan \
  memberships.planfeature \
  --indent 2 \
  > production_data.json
```

### Step 2: Download the JSON File

1. Use cPanel File Manager
2. Navigate to `/home/magmafit/magma7_proj/`
3. Find `production_data.json`
4. Download it
5. Place it in your local project root: `/Users/Apple/projects/magma7_proj/`

### Step 3: Import to Local SQLite

On your local Mac:

```bash
cd /Users/Apple/projects/magma7_proj
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development

# Backup current database
cp db.sqlite3 db.sqlite3.backup

# Load production data
python manage.py loaddata production_data.json
```

Done! ✓

---

## Alternative Method: Manual SQL Import

If you want to use the existing MySQL dump file, here's how:

### Step 1: Install MySQL to SQLite Converter

```bash
pip install mysql-to-sqlite3
```

### Step 2: Convert and Import

```bash
# This tool doesn't work well with Django databases
# Better to use the JSON method above
```

---

## What Gets Imported

This imports **content only** (not users, sessions, or auth data):

✅ **Site Settings** - Logo, colors, text
✅ **Hero Slides** - Homepage slider images
✅ **Programs** - Fitness programs
✅ **Services** - Why choose us items
✅ **Partners** - Partner logos
✅ **Testimonials** - Customer reviews
✅ **Media Assets** - Uploaded images/files
✅ **Home Gallery** - Facility gallery images
✅ **About Page** - Content and images
✅ **Facilities** - Facility information
✅ **Team Members** - Staff profiles
✅ **Membership Plans** - Pricing plans and features

❌ **NOT Imported:**
- User accounts (create fresh locally)
- Subscriptions (testing data)
- Payments (sensitive data)
- Sessions
- Error logs

---

## After Import

### Verify Data

```bash
python manage.py shell
```

```python
from cms.models import *
from memberships.models import Plan

print(f"Site Settings: {SiteSettings.objects.count()}")
print(f"Hero Slides: {HeroSlide.objects.count()}")
print(f"Programs: {Program.objects.count()}")
print(f"Services: {Service.objects.count()}")
print(f"Plans: {Plan.objects.count()}")
print(f"Home Gallery: {HomeGalleryImage.objects.count()}")

# List plans
for plan in Plan.objects.all():
    print(f"  - {plan.name}: ₦{plan.price}")
```

### Create Local Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@local.dev`
- Password: `admin123` (for local only!)

### Run Dev Server

```bash
python manage.py runserver
```

Visit:
- Homepage: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`

---

## Troubleshooting

### Error: "No such table"

Run migrations first:
```bash
python manage.py migrate
```

### Error: "Duplicate entry"

Clear existing data:
```bash
python manage.py shell
```
```python
from cms.models import *
from memberships.models import *

# Delete existing data
Plan.objects.all().delete()
PlanFeature.objects.all().delete()
HeroSlide.objects.all().delete()
# ... etc
```

Then try loaddata again.

### Data looks wrong

Make sure you're using:
```bash
export DJANGO_SETTINGS_MODULE=magma7.settings.development
```

Not production settings on local machine.

### Images not showing

Images are stored as URLs, not files. You have two options:

**Option 1: Update URLs to production**
- Images will load from production server
- No need to download actual image files

**Option 2: Download images**
1. Download `/home/magmafit/magma7_proj/media/` from cPanel
2. Place in `/Users/Apple/projects/magma7_proj/media/`
3. Update `MediaAsset` URLs to point to local files

---

## Quick Import Script

Create this file: `import_production_data.sh`

```bash
#!/bin/bash

echo "Importing production data to local SQLite..."
echo ""

# Backup
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

# Import
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development

if [ ! -f "production_data.json" ]; then
    echo "Error: production_data.json not found!"
    echo ""
    echo "Download it from production server first:"
    echo "  1. SSH to cPanel"
    echo "  2. Run: python manage.py dumpdata ... > production_data.json"
    echo "  3. Download the file"
    echo "  4. Place it in project root"
    exit 1
fi

python manage.py loaddata production_data.json

echo ""
echo "✓ Import complete!"
echo ""
echo "Verify:"
python manage.py shell -c "
from cms.models import *
from memberships.models import Plan
print(f'Plans: {Plan.objects.count()}')
print(f'Hero Slides: {HeroSlide.objects.count()}')
print(f'Programs: {Program.objects.count()}')
"

echo ""
echo "Next: python manage.py runserver"
```

Make it executable:
```bash
chmod +x import_production_data.sh
```

Run it:
```bash
./import_production_data.sh
```

---

## Summary

**Recommended approach:**
1. Export from production: `python manage.py dumpdata ... > production_data.json`
2. Download JSON file
3. Import locally: `python manage.py loaddata production_data.json`

**Time:** 5 minutes

**Safe:** ✓ Only imports content, not sensitive data

**Reversible:** ✓ Backup created automatically

---

**Status:** Ready to import ✓
