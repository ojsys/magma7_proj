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

def upd(cursor, sql, label):
    try:
        cursor.execute(sql)
        print(f"  {label}: {cursor.rowcount} row(s)")
    except Exception as e:
        print(f"  {label}: {e}")

print("Normalizing boolean values (strings -> integers)...")
with connection.cursor() as cursor:
    # memberships_plan
    print("\nFix: memberships_plan")
    upd(cursor, "UPDATE memberships_plan SET is_featured = 0 WHERE is_featured IN ('0','false','False','') OR is_featured IS NULL;", "is_featured -> 0")
    upd(cursor, "UPDATE memberships_plan SET is_featured = 1 WHERE is_featured IN ('1','true','True');", "is_featured -> 1")
    upd(cursor, "UPDATE memberships_plan SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE memberships_plan SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # memberships_weeklygoal
    print("\nFix: memberships_weeklygoal")
    upd(cursor, "UPDATE memberships_weeklygoal SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE memberships_weeklygoal SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_errorlog
    print("\nFix: cms_errorlog")
    upd(cursor, "UPDATE cms_errorlog SET resolved = 0 WHERE resolved IN ('0','false','False','') OR resolved IS NULL;", "resolved -> 0")
    upd(cursor, "UPDATE cms_errorlog SET resolved = 1 WHERE resolved IN ('1','true','True');", "resolved -> 1")

    # cms_heroslide
    print("\nFix: cms_heroslide")
    upd(cursor, "UPDATE cms_heroslide SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_heroslide SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_aboutgalleryimage
    print("\nFix: cms_aboutgalleryimage")
    upd(cursor, "UPDATE cms_aboutgalleryimage SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_aboutgalleryimage SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_corevalue
    print("\nFix: cms_corevalue")
    upd(cursor, "UPDATE cms_corevalue SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_corevalue SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_whychooseusitem
    print("\nFix: cms_whychooseusitem")
    upd(cursor, "UPDATE cms_whychooseusitem SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_whychooseusitem SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_aboutstatistic
    print("\nFix: cms_aboutstatistic")
    upd(cursor, "UPDATE cms_aboutstatistic SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_aboutstatistic SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")

    # cms_facility
    print("\nFix: cms_facility")
    upd(cursor, "UPDATE cms_facility SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_facility SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")
    upd(cursor, "UPDATE cms_facility SET is_featured = 0 WHERE is_featured IN ('0','false','False','') OR is_featured IS NULL;", "is_featured -> 0")
    upd(cursor, "UPDATE cms_facility SET is_featured = 1 WHERE is_featured IN ('1','true','True');", "is_featured -> 1")

    # cms_teammember
    print("\nFix: cms_teammember")
    upd(cursor, "UPDATE cms_teammember SET is_active = 0 WHERE is_active IN ('0','false','False','') OR is_active IS NULL;", "is_active -> 0")
    upd(cursor, "UPDATE cms_teammember SET is_active = 1 WHERE is_active IN ('1','true','True');", "is_active -> 1")
    upd(cursor, "UPDATE cms_teammember SET is_featured = 0 WHERE is_featured IN ('0','false','False','') OR is_featured IS NULL;", "is_featured -> 0")
    upd(cursor, "UPDATE cms_teammember SET is_featured = 1 WHERE is_featured IN ('1','true','True');", "is_featured -> 1")

    # cms_testimonial
    print("\nFix: cms_testimonial")
    upd(cursor, "UPDATE cms_testimonial SET is_approved = 0 WHERE is_approved IN ('0','false','False','') OR is_approved IS NULL;", "is_approved -> 0")
    upd(cursor, "UPDATE cms_testimonial SET is_approved = 1 WHERE is_approved IN ('1','true','True');", "is_approved -> 1")

print("\n✓ Boolean values normalized")
PYEOF

echo ""
echo "Step 1b: Converting TEXT boolean columns to TINYINT(1) ..."
echo "---------------------------------------"
python manage.py shell << 'PYEOF'
from django.db import connection

def ddl(cursor, sql):
    try:
        cursor.execute(sql)
        print(f"  OK: {sql}")
    except Exception as e:
        print(f"  SKIP: {sql} -> {e}")

with connection.cursor() as cursor:
    # memberships
    ddl(cursor, "ALTER TABLE memberships_plan MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE memberships_plan MODIFY is_featured TINYINT(1) NOT NULL DEFAULT 0;")
    ddl(cursor, "ALTER TABLE memberships_weeklygoal MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")

    # cms tables
    ddl(cursor, "ALTER TABLE cms_heroslide MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_aboutgalleryimage MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_corevalue MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_whychooseusitem MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_aboutstatistic MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_facility MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_facility MODIFY is_featured TINYINT(1) NOT NULL DEFAULT 0;")
    ddl(cursor, "ALTER TABLE cms_teammember MODIFY is_active TINYINT(1) NOT NULL DEFAULT 1;")
    ddl(cursor, "ALTER TABLE cms_teammember MODIFY is_featured TINYINT(1) NOT NULL DEFAULT 0;")
    ddl(cursor, "ALTER TABLE cms_testimonial MODIFY is_approved TINYINT(1) NOT NULL DEFAULT 1;")

print("\n✓ Column types converted where needed")
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
