#!/bin/bash
# Import production data to local SQLite database

echo "=========================================="
echo "Import Production Data to Local SQLite"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.development

echo "This will:"
echo "  1. Backup your current db.sqlite3"
echo "  2. Clear existing data from key tables"
echo "  3. Import production data"
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Step 1: Backing up current database..."
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

echo ""
echo "Step 2: Running Python import script..."
python import_mysql_to_sqlite.py

echo ""
echo "Step 3: Verifying data..."
python manage.py shell << 'EOF'
from memberships.models import Plan
from cms.models import HeroSlide, SiteSettings, Program, Service

print("\n=== Data Verification ===")
print(f"Plans: {Plan.objects.count()}")
print(f"Hero Slides: {HeroSlide.objects.count()}")
print(f"Programs: {Program.objects.count()}")
print(f"Services: {Service.objects.count()}")
print(f"Site Settings: {SiteSettings.objects.count()}")
print("\n✓ Verification complete")
EOF

echo ""
echo "=========================================="
echo "✓ Import complete!"
echo "=========================================="
echo ""
echo "Next: Run 'python manage.py runserver' to test"
echo ""
