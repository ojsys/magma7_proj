#!/bin/bash
# Quick script to import production data to local SQLite

echo "=========================================="
echo "Import Production Data to Local"
echo "=========================================="
echo ""

# Check if production_data.json exists
if [ ! -f "production_data.json" ]; then
    echo "❌ Error: production_data.json not found!"
    echo ""
    echo "You need to export data from production first."
    echo ""
    echo "Run this on your cPanel Terminal:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "cd /home/magmafit/magma7_proj"
    echo "source ~/virtualenv/magma7_proj/3.12/bin/activate"
    echo "export DJANGO_SETTINGS_MODULE=magma7.settings.production"
    echo ""
    echo "python manage.py dumpdata \\"
    echo "  cms.sitesettings \\"
    echo "  cms.heroslide \\"
    echo "  cms.program \\"
    echo "  cms.service \\"
    echo "  cms.partner \\"
    echo "  cms.testimonial \\"
    echo "  cms.mediaasset \\"
    echo "  cms.homegalleryimage \\"
    echo "  cms.aboutpage \\"
    echo "  cms.corevalue \\"
    echo "  cms.whychooseusitem \\"
    echo "  cms.aboutgalleryimage \\"
    echo "  cms.aboutstatistic \\"
    echo "  cms.facility \\"
    echo "  cms.teammember \\"
    echo "  cms.facilitiespage \\"
    echo "  cms.teampage \\"
    echo "  memberships.plan \\"
    echo "  memberships.planfeature \\"
    echo "  --indent 2 > production_data.json"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Then download production_data.json from cPanel"
    echo "and place it in this directory."
    echo ""
    exit 1
fi

echo "Found: production_data.json ✓"
echo ""
echo "This will import production data into your local database."
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Step 1: Creating backup..."
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || echo "No existing database to backup"
echo "✓ Backup created (if database existed)"

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development
echo "✓ Environment ready"

echo ""
echo "Step 3: Running migrations..."
python manage.py migrate --noinput
echo "✓ Migrations complete"

echo ""
echo "Step 4: Importing production data..."
python manage.py loaddata production_data.json

echo ""
echo "Step 5: Verifying data..."
python manage.py shell << 'EOF'
from cms.models import *
from memberships.models import Plan

print("\n" + "="*60)
print("DATA VERIFICATION")
print("="*60)

items = [
    ("Site Settings", SiteSettings.objects.count()),
    ("Hero Slides", HeroSlide.objects.count()),
    ("Programs", Program.objects.count()),
    ("Services", Service.objects.count()),
    ("Partners", Partner.objects.count()),
    ("Testimonials", Testimonial.objects.count()),
    ("Media Assets", MediaAsset.objects.count()),
    ("Home Gallery Images", HomeGalleryImage.objects.count()),
    ("Membership Plans", Plan.objects.count()),
    ("Facilities", Facility.objects.count()),
    ("Team Members", TeamMember.objects.count()),
]

for name, count in items:
    print(f"  {name}: {count}")

print("\nMembership Plans:")
for plan in Plan.objects.all():
    print(f"  - {plan.name}: ₦{plan.price:,}")

print("\n" + "="*60)
print("✓ Verification Complete")
print("="*60)
EOF

echo ""
echo "=========================================="
echo "✓ Import Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Create superuser: python manage.py createsuperuser"
echo "  2. Run server: python manage.py runserver"
echo "  3. Visit: http://localhost:8000/"
echo ""
