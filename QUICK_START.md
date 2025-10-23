# Quick Start Guide - Magma7Fitness Local Development

## Start Development Server

```bash
cd /Users/Apple/projects/magma7_proj
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development
python manage.py runserver
```

**Visit:** http://localhost:8000/

---

## Admin Access

**URL:** http://localhost:8000/admin/

**Credentials:**
- Username: `admin`
- Password: `admin123`

---

## Common Commands

### Database
```bash
# Run migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic
```

### Import/Export Data
```bash
# Import production data
bash import_production_now.sh

# Export to production (run on cPanel)
bash export_production_data.sh
```

---

## Deployment to Production

### Quick Fix Checklist

**Upload files via cPanel File Manager:**
1. Modified Python files → `/home/magmafit/magma7_proj/`
2. Templates → `/home/magmafit/magma7_proj/core/templates/`
3. Static CSS → `/home/magmafit/magma7_proj/static/css/`
4. Migrations → `/home/magmafit/magma7_proj/cms/migrations/`

**Run in cPanel Terminal:**
```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Run migrations
python manage.py migrate cms

# Collect static
python manage.py collectstatic --noinput

# Restart app
touch passenger_wsgi.py
```

---

## Project Structure

```
magma7_proj/
├── cms/              # CMS models (content management)
├── core/             # Main app (views, templates)
├── memberships/      # Membership plans
├── payments/         # Paystack integration
├── users/            # Custom user model
├── notifications/    # Email notifications
├── magma7/          # Project settings
│   └── settings/    # Split settings (base, dev, prod)
├── static/          # CSS, JS, images
├── media/           # Uploaded files
└── templates/       # Base templates
```

---

## Current Features

✓ Homepage with hero slider
✓ Programs showcase
✓ Services/Why Choose Us
✓ Membership plans
✓ About page with gallery
✓ Facilities page
✓ Team page
✓ Testimonials
✓ Media Center (admin)
✓ Contact page
✓ User authentication
✓ Membership subscriptions
✓ Paystack payment integration
✓ Admin CMS for all content

---

## Recent Updates

### Navigation Complete Redesign (NEW!)
Complete rebuild with modern, responsive navigation.

**Files Changed:**
- `templates/base.html` - New navbar HTML
- `static/css/styles.css` - Custom navigation CSS
- JavaScript added for mobile menu

**Features:**
- Perfect spacing on desktop
- Smooth animations
- Modern mobile menu (full-screen)
- Sticky navbar
- Notification badge

**See:** `DEPLOY_NEW_NAVBAR.md` for details

### Home Gallery Feature
Added facility gallery section on homepage.

**Models:** `cms.models.HomeGalleryImage`
**Admin:** `/admin/cms/homegalleryimage/`
**Template:** `core/templates/core/home.html`

### Production Data Import
Created scripts to sync production data to local development.

**Scripts:**
- `import_production_now.sh` - Auto import
- `export_production_data.sh` - Export from production

---

## Pending Production Tasks

### 1. Fix Migration Conflict
```bash
# On cPanel Terminal
python manage.py migrate cms 0007_errorlog --fake
python manage.py migrate cms
touch passenger_wsgi.py
```

### 2. Deploy Mobile Menu Fix
```bash
# Upload: static/css/styles.css
python manage.py collectstatic --noinput
touch passenger_wsgi.py
```

### 3. Add Gallery Images
Once migrations run, add facility photos at:
`/admin/cms/homegalleryimage/`

---

## Key URLs

### Local
- Homepage: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- Plans: http://localhost:8000/memberships/plans/
- About: http://localhost:8000/about/
- Facilities: http://localhost:8000/facilities/

### Production
- Homepage: https://www.magma7fitness.com/
- Admin: https://www.magma7fitness.com/admin/
- Plans: https://www.magma7fitness.com/memberships/plans/

---

## Documentation Files

- `HOME_GALLERY_GUIDE.md` - Gallery feature docs
- `DEPLOY_HOME_GALLERY.md` - Gallery deployment
- `DEPLOY_MOBILE_MENU_FIX.md` - Menu fix deployment
- `IMPORT_PRODUCTION_DATA.md` - Data import guide
- `IMPORT_SUCCESS.md` - Import verification
- `CPANEL_403_FIX.md` - 403 error troubleshooting

---

## Contact & Support

**Production Site:** https://www.magma7fitness.com/
**Email:** info@magma7fitness.com
**Phone:** +234 000 000 0000

---

**Last Updated:** October 22, 2025
