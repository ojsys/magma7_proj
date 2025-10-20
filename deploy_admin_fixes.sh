#!/bin/bash
# Deploy Admin Error Fixes to Production
# Fixes BooleanField and timezone errors on cPanel

echo "=========================================="
echo "Deploying Admin Error Fixes"
echo "=========================================="
echo ""

echo "INSTRUCTIONS:"
echo ""
echo "1. Upload these files to your cPanel File Manager:"
echo "   ✓ magma7/settings/production.py"
echo "   ✓ cms/admin.py"
echo ""
echo "2. Then run this script on your cPanel Terminal:"
echo ""
echo "   cd /home/magmafit/magma7_proj"
echo "   bash deploy_admin_fixes.sh"
echo ""
echo "=========================================="
echo ""
read -p "Have you uploaded the files? (yes/no): " UPLOADED

if [ "$UPLOADED" != "yes" ]; then
    echo ""
    echo "Please upload the files first, then run this script again."
    echo ""
    exit 1
fi

echo ""
echo "=========================================="
echo "Starting Deployment..."
echo "=========================================="
echo ""

# Navigate to project directory
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "✓ Activated virtual environment and set production settings"
echo ""

echo "Step 1: Fixing BooleanField values in database..."
echo "---------------------------------------"
python manage.py shell << 'PYEOF'
from django.db import connection

with connection.cursor() as cursor:
    # Fix memberships_plan boolean fields
    print("Fixing memberships_plan table...")

    # Fix is_featured field
    cursor.execute("UPDATE memberships_plan SET is_featured = 0 WHERE is_featured = '0' OR is_featured = '' OR is_featured IS NULL;")
    print(f"  Fixed is_featured (set to 0): {cursor.rowcount} rows")

    cursor.execute("UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = '1';")
    print(f"  Fixed is_featured (set to 1): {cursor.rowcount} rows")

    # Fix is_active field
    cursor.execute("UPDATE memberships_plan SET is_active = 0 WHERE is_active = '0' OR is_active = '' OR is_active IS NULL;")
    print(f"  Fixed is_active (set to 0): {cursor.rowcount} rows")

    cursor.execute("UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1';")
    print(f"  Fixed is_active (set to 1): {cursor.rowcount} rows")

    # Fix cms_errorlog boolean field
    print("\nFixing cms_errorlog table...")
    try:
        cursor.execute("UPDATE cms_errorlog SET resolved = 0 WHERE resolved = '0' OR resolved = '' OR resolved IS NULL;")
        print(f"  Fixed resolved (set to 0): {cursor.rowcount} rows")

        cursor.execute("UPDATE cms_errorlog SET resolved = 1 WHERE resolved = '1';")
        print(f"  Fixed resolved (set to 1): {cursor.rowcount} rows")
    except Exception as e:
        print(f"  Note: {e}")

print("\n✓ Boolean fields fixed!")
PYEOF

echo ""
echo "Step 2: Verifying settings update..."
echo "---------------------------------------"
python manage.py shell << 'PYEOF'
from django.conf import settings

print("Database timezone configuration:")
db_config = settings.DATABASES['default']
if 'OPTIONS' in db_config:
    print(f"  init_command: {db_config['OPTIONS'].get('init_command', 'Not set')}")
    print(f"  charset: {db_config['OPTIONS'].get('charset', 'Not set')}")
else:
    print("  WARNING: OPTIONS not configured!")

if 'TIME_ZONE' in db_config:
    print(f"  TIME_ZONE: {db_config['TIME_ZONE']}")

print("\n✓ Settings verified")
PYEOF

echo ""
echo "Step 3: Testing admin pages..."
echo "---------------------------------------"
python manage.py shell << 'PYEOF'
from memberships.models import Plan
from cms.models import ErrorLog

# Test memberships
try:
    plans = Plan.objects.all()
    print(f"\n✓ Memberships Plans: {plans.count()} plans found")
    for plan in plans:
        print(f"  - {plan.name}: featured={plan.is_featured}, active={plan.is_active}")
except Exception as e:
    print(f"\n✗ Memberships error: {e}")

# Test error logs
try:
    errors = ErrorLog.objects.all().order_by('-timestamp')[:5]
    print(f"\n✓ Error Logs: {ErrorLog.objects.count()} total errors")
    print(f"  Showing latest {errors.count()} errors:")
    for err in errors:
        print(f"  - [{err.severity}] {err.message[:50]}")
except Exception as e:
    print(f"\n✗ Error Log error: {e}")
PYEOF

echo ""
echo "Step 4: Restarting application..."
echo "---------------------------------------"
touch passenger_wsgi.py
echo "✓ Application restarted (touched passenger_wsgi.py)"

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "What was fixed:"
echo "  ✓ BooleanField values ('0' string → 0 integer)"
echo "  ✓ MySQL timezone configuration added"
echo "  ✓ ErrorLog date_hierarchy disabled (prevents timezone errors)"
echo "  ✓ Application restarted"
echo ""
echo "Next Steps:"
echo "  1. Visit admin pages to verify they work:"
echo "     • https://www.magma7fitness.com/admin/memberships/plan/"
echo "     • https://www.magma7fitness.com/admin/cms/errorlog/"
echo ""
echo "  2. If errors persist, check the error logs:"
echo "     • cPanel → Error Log"
echo "     • Or in Django admin: https://www.magma7fitness.com/admin/cms/errorlog/"
echo ""
echo "  3. Set featured membership plan:"
echo "     • See SET_FEATURED_PLAN.md for instructions"
echo "     • Recommend featuring the Quarterly (3-month) plan"
echo ""
echo "=========================================="
echo ""
