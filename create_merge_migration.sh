#!/bin/bash
# Create proper merge migration

echo "=========================================="
echo "Creating Merge Migration"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Create a clean merge migration manually
echo "1. Creating merge migration..."
cat > cms/migrations/0011_merge_fix.py << 'PYEOF'
# Merge migration to fix conflicting branches

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_heroslide'),
        ('cms', '0010_alter_mediaasset_options_and_more'),
    ]

    operations = [
        # No operations needed - this just merges the two branches
    ]
PYEOF

echo "✓ Created 0011_merge_fix.py"

# Show migration status
echo ""
echo "2. Checking migrations..."
python manage.py showmigrations cms

# Run migrations
echo ""
echo "3. Running migrations..."
python manage.py migrate cms

# Verify ErrorLog table
echo ""
echo "4. Verifying ErrorLog table..."
python manage.py shell << 'PYEOF'
from cms.models import ErrorLog
try:
    count = ErrorLog.objects.count()
    print(f"\n✓ SUCCESS! ErrorLog table created! Current entries: {count}\n")
except Exception as e:
    print(f"\n✗ Error: {e}\n")
PYEOF

# Test error logging
echo ""
echo "5. Testing error log functionality..."
python manage.py shell << 'PYEOF'
from cms.models import ErrorLog
from django.utils import timezone

# Create a test error log entry
test_error = ErrorLog.objects.create(
    severity='INFO',
    message='Test error log entry - system is working!',
    path='/test/',
    method='GET',
    user='System',
    resolved=False
)

print(f"✓ Test error created with ID: {test_error.id}")
print(f"✓ Total errors in log: {ErrorLog.objects.count()}")
PYEOF

# Restart application
echo ""
echo "6. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Error Log System Ready!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Visit: https://www.magma7fitness.com/admin/"
echo "2. Go to 'Error Logs' in CMS section"
echo "3. You should see your test error entry"
echo ""
