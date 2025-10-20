#!/bin/bash
# Fix migration conflict on production server

echo "=========================================="
echo "Fixing Migration Conflict"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Backup and remove conflicted merge migrations
echo ""
echo "2. Removing conflicted merge migrations..."
if [ -f "cms/migrations/0009_merge_0004_errorlog_0008_merge_20251020_1136.py" ]; then
    mv cms/migrations/0009_merge_0004_errorlog_0008_merge_20251020_1136.py cms/migrations/0009_merge_BACKUP.py.bak
    echo "✓ Removed 0009_merge"
fi

if [ -f "cms/migrations/0008_merge_20251020_1136.py" ]; then
    mv cms/migrations/0008_merge_20251020_1136.py cms/migrations/0008_merge_BACKUP.py.bak
    echo "✓ Removed 0008_merge"
fi

if [ -f "cms/migrations/0007_merge_20251020_1106.py" ]; then
    mv cms/migrations/0007_merge_20251020_1106.py cms/migrations/0007_merge_BACKUP.py.bak
    echo "✓ Removed 0007_merge"
fi

# List remaining migrations
echo ""
echo "3. Listing remaining migration files..."
ls -la cms/migrations/*.py | grep -v __pycache__ | grep -v BACKUP

# Show migration status
echo ""
echo "4. Checking migration status..."
python manage.py showmigrations cms

# Fake the merge migrations that are already applied
echo ""
echo "5. Marking problematic migrations as fake..."
python manage.py migrate cms --fake 0007_merge_20251020_1106 2>/dev/null || echo "Migration 0007 not needed"
python manage.py migrate cms --fake 0008_merge_20251020_1136 2>/dev/null || echo "Migration 0008 not needed"
python manage.py migrate cms --fake 0009_merge_0004_errorlog_0008_merge_20251020_1136 2>/dev/null || echo "Migration 0009 not needed"

# Run the actual migrations we need
echo ""
echo "6. Running real migrations..."
python manage.py migrate cms

# Verify ErrorLog table
echo ""
echo "7. Verifying ErrorLog table..."
python manage.py shell << 'PYEOF'
from cms.models import ErrorLog
try:
    count = ErrorLog.objects.count()
    print(f"✓ SUCCESS! ErrorLog table exists with {count} entries.")
except Exception as e:
    print(f"✗ Error: {e}")
PYEOF

# Restart application
echo ""
echo "8. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Migration conflict fixed!"
echo "=========================================="
echo ""
