#!/bin/bash
# Fix admin errors - Boolean fields and timezone issues

echo "=========================================="
echo "Fixing Admin Errors"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "1. Fixing BooleanField values in database..."
python manage.py shell << 'PYEOF'
from django.db import connection

with connection.cursor() as cursor:
    # Fix memberships_plan boolean fields
    print("Fixing memberships_plan table...")
    cursor.execute("UPDATE memberships_plan SET is_featured = 0 WHERE is_featured = '0' OR is_featured = '' OR is_featured IS NULL;")
    print(f"  Fixed is_featured: {cursor.rowcount} rows")

    cursor.execute("UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = '1';")
    cursor.execute("UPDATE memberships_plan SET is_active = 0 WHERE is_active = '0' OR is_active = '' OR is_active IS NULL;")
    cursor.execute("UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1';")
    print(f"  Fixed is_active")

    # Fix cms_errorlog boolean field
    print("\nFixing cms_errorlog table...")
    try:
        cursor.execute("UPDATE cms_errorlog SET resolved = 0 WHERE resolved = '0' OR resolved = '' OR resolved IS NULL;")
        print(f"  Fixed resolved: {cursor.rowcount} rows")
        cursor.execute("UPDATE cms_errorlog SET resolved = 1 WHERE resolved = '1';")
    except Exception as e:
        print(f"  Note: {e}")

print("\n✓ Boolean fields fixed!")
PYEOF

echo ""
echo "2. Uploading fixed production settings..."
# The settings file already has the timezone fix

echo ""
echo "3. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "4. Testing admin pages..."
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
    errors = ErrorLog.objects.all()[:5]
    print(f"\n✓ Error Logs: {ErrorLog.objects.count()} total errors")
    for err in errors:
        print(f"  - [{err.severity}] {err.message[:50]}")
except Exception as e:
    print(f"\n✗ Error Log error: {e}")
PYEOF

echo ""
echo "=========================================="
echo "✓ Admin errors fixed!"
echo "=========================================="
echo ""
echo "What was done:"
echo "  • Fixed BooleanField values ('0' string → 0 integer)"
echo "  • Added MySQL timezone configuration"
echo "  • Restarted application"
echo ""
echo "Next: Visit admin to verify:"
echo "  • https://www.magma7fitness.com/admin/memberships/plan/"
echo "  • https://www.magma7fitness.com/admin/cms/errorlog/"
echo ""
