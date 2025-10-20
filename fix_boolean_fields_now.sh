#!/bin/bash
# Quick fix for boolean fields on production - run this NOW

echo "=========================================="
echo "Quick Boolean Field Fix"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "Fixing boolean fields in database..."
echo ""

python manage.py shell << 'PYEOF'
from django.db import connection

print("Connecting to database...")

with connection.cursor() as cursor:
    # Fix memberships_plan boolean fields
    print("\n1. Fixing memberships_plan table...")

    # First, let's see what we have
    cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
    rows = cursor.fetchall()
    print(f"\nCurrent data ({len(rows)} plans):")
    for row in rows:
        print(f"  ID: {row[0]}, Name: {row[1]}, is_featured: '{row[2]}', is_active: '{row[3]}'")

    # Fix is_featured - convert all string values to integers
    print("\nFixing is_featured field...")
    cursor.execute("UPDATE memberships_plan SET is_featured = 0 WHERE is_featured != 1;")
    print(f"  Set {cursor.rowcount} rows to 0")

    cursor.execute("UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = '1';")
    print(f"  Set {cursor.rowcount} rows to 1")

    # Fix is_active - convert all string values to integers
    print("\nFixing is_active field...")
    cursor.execute("UPDATE memberships_plan SET is_active = 0 WHERE is_active != 1;")
    print(f"  Set {cursor.rowcount} rows to 0")

    cursor.execute("UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1';")
    print(f"  Set {cursor.rowcount} rows to 1")

    # Verify the fix
    print("\nVerifying fix...")
    cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
    rows = cursor.fetchall()
    print(f"\nFixed data ({len(rows)} plans):")
    for row in rows:
        print(f"  ID: {row[0]}, Name: {row[1]}, is_featured: {row[2]}, is_active: {row[3]}")

print("\n✓ Boolean fields fixed!")
print("\nNOTE: Values should now be 0 or 1 (not '0' or '1' with quotes)")
PYEOF

echo ""
echo "Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Fix complete!"
echo "=========================================="
echo ""
echo "Now test the admin page:"
echo "https://www.magma7fitness.com/admin/memberships/plan/"
echo ""
