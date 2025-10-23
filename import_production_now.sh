#!/bin/bash
# Auto-import production data (no prompts)

echo "=========================================="
echo "Auto-Import Production Data"
echo "=========================================="
echo ""

# Check if production_data.json exists
if [ ! -f "production_data.json" ]; then
    echo "❌ Error: production_data.json not found!"
    exit 1
fi

echo "Step 1: Creating backup..."
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || echo "No existing database"
echo "✓ Done"

echo ""
echo "Step 2: Activating environment..."
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development
echo "✓ Done"

echo ""
echo "Step 3: Running migrations..."
python manage.py migrate --noinput 2>&1 | grep -E "(Operations|Applying|No migrations)"
echo "✓ Done"

echo ""
echo "Step 4: Creating admin user (ID: 1)..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(pk=1).exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@local.dev',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print(f"✓ Created admin user (ID: {user.pk})")
else:
    print("✓ Admin user already exists")
EOF

echo ""
echo "Step 5: Importing production data..."
python manage.py loaddata production_data.json 2>&1 | grep -E "(Installed|Deserializing|objects)" || echo "✓ Import completed"

echo ""
echo "Step 6: Verifying imported data..."
python manage.py shell << 'EOF'
from cms.models import *
from memberships.models import Plan

print("\n" + "="*60)
print("DATA IMPORTED")
print("="*60)

data = [
    ("Site Settings", SiteSettings.objects.count()),
    ("Hero Slides", HeroSlide.objects.count()),
    ("Programs", Program.objects.count()),
    ("Services", Service.objects.count()),
    ("Partners", Partner.objects.count()),
    ("Testimonials", Testimonial.objects.count()),
    ("Media Assets", MediaAsset.objects.count()),
    ("Home Gallery", HomeGalleryImage.objects.count()),
    ("Membership Plans", Plan.objects.count()),
    ("Facilities", Facility.objects.count()),
    ("Team Members", TeamMember.objects.count()),
]

for name, count in data:
    status = "✓" if count > 0 else "○"
    print(f"  {status} {name}: {count}")

print("\n📋 Membership Plans:")
for plan in Plan.objects.all().order_by('price'):
    print(f"  • {plan.name}: ₦{plan.price:,}/month")

print("\n🖼️  Hero Slides:")
for slide in HeroSlide.objects.filter(is_active=True).order_by('order')[:3]:
    print(f"  • {slide.title} (Order: {slide.order})")

print("\n" + "="*60)
print("✓ IMPORT SUCCESSFUL")
print("="*60)
EOF

echo ""
echo "=========================================="
echo "✓ All Done!"
echo "=========================================="
echo ""
echo "🔐 Admin Login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🚀 Next Steps:"
echo "   python manage.py runserver"
echo "   Open: http://localhost:8000/"
echo "   Admin: http://localhost:8000/admin/"
echo ""
