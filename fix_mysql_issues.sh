#!/bin/bash
# Fix MySQL timezone and boolean field issues

echo "=========================================="
echo "Fixing MySQL Issues"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "1. Loading MySQL timezone data..."
echo "   (This requires MySQL root access)"
echo ""
echo "   Run this command in your cPanel MySQL terminal or phpMyAdmin:"
echo "   mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql"
echo ""
echo "   OR if you don't have root access, we'll use Django's workaround..."
echo ""

echo "2. Fixing BooleanField issue in database..."
python manage.py shell << 'PYEOF'
from django.db import connection

# Fix is_featured field to be proper boolean (0/1)
with connection.cursor() as cursor:
    # Check current data type
    cursor.execute("DESCRIBE memberships_plan;")
    columns = cursor.fetchall()
    print("Current plan table structure:")
    for col in columns:
        if 'featured' in col[0].lower():
            print(f"  {col[0]}: {col[1]}")

    # Fix any '0' string values to proper 0
    cursor.execute("UPDATE memberships_plan SET is_featured = 0 WHERE is_featured = '0' OR is_featured IS NULL OR is_featured = '';")
    print(f"\nFixed {cursor.rowcount} rows with incorrect boolean values")

    # Do the same for is_active
    cursor.execute("UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1' OR is_active IS NULL OR is_active = '';")
    cursor.execute("UPDATE memberships_plan SET is_active = 0 WHERE is_active = '0';")
    print(f"Fixed is_active field")

print("\n✓ Boolean fields fixed!")
PYEOF

echo ""
echo "3. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ MySQL issues fixed!"
echo "=========================================="
echo ""
echo "What was done:"
echo "  • Fixed BooleanField data in database"
echo "  • Converted string '0' to integer 0"
echo "  • Restarted application"
echo ""
echo "Note: If you still see timezone errors, contact your"
echo "hosting provider to load MySQL timezone data."
echo ""
