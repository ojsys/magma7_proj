#!/bin/bash
# Safe import of production data - handles foreign key issues

echo "=========================================="
echo "Safe Import Production Data to Local"
echo "=========================================="
echo ""

# Check if production_data.json exists
if [ ! -f "production_data.json" ]; then
    echo "❌ Error: production_data.json not found!"
    echo ""
    echo "Please download production_data.json from cPanel first."
    echo ""
    exit 1
fi

echo "Found: production_data.json ✓"
echo ""
echo "This will import production data into your local database."
echo "A temporary admin user will be created to satisfy foreign key constraints."
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
echo "Step 4: Creating temporary admin user..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

# Create temporary admin user with ID 1 to satisfy foreign keys
if not User.objects.filter(pk=1).exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@local.dev',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print(f"✓ Created temporary admin user (ID: {user.pk})")
else:
    print("✓ Admin user already exists")
EOF

echo ""
echo "Step 5: Importing production data..."
python manage.py loaddata production_data.json

echo ""
echo "Step 6: Verifying data..."
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
    ("About Page", AboutPage.objects.count()),
    ("Core Values", CoreValue.objects.count()),
    ("Why Choose Us Items", WhyChooseUsItem.objects.count()),
]

for name, count in items:
    print(f"  {name}: {count}")

print("\nMembership Plans:")
for plan in Plan.objects.all():
    print(f"  - {plan.name}: ₦{plan.price:,}")

print("\nHero Slides:")
for slide in HeroSlide.objects.filter(is_active=True).order_by('order')[:5]:
    print(f"  - {slide.title} (Order: {slide.order})")

print("\n" + "="*60)
print("✓ Verification Complete")
print("="*60)
EOF

echo ""
echo "=========================================="
echo "✓ Import Complete!"
echo "=========================================="
echo ""
echo "Imported data:"
echo "  ✓ Site settings and branding"
echo "  ✓ Hero slides"
echo "  ✓ Programs and services"
echo "  ✓ Membership plans"
echo "  ✓ Testimonials and partners"
echo "  ✓ Media assets"
echo "  ✓ About page content"
echo "  ✓ Facilities and team members"
echo ""
echo "Admin Login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Next steps:"
echo "  1. Run server: python manage.py runserver"
echo "  2. Visit: http://localhost:8000/"
echo "  3. Admin: http://localhost:8000/admin/"
echo "  4. (Optional) Change admin password or create new superuser"
echo ""
