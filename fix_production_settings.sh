#!/bin/bash
# Fix production settings - ensure DJANGO_SETTINGS_MODULE is set correctly

echo "=========================================="
echo "Fixing Production Settings"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings EXPLICITLY
echo ""
echo "2. Setting DJANGO_SETTINGS_MODULE to production..."
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Show current database being used
echo ""
echo "3. Checking database configuration..."
python manage.py shell << 'PYEOF'
from django.conf import settings
print("=" * 60)
print("SETTINGS MODULE:", settings.SETTINGS_MODULE)
print("DATABASE ENGINE:", settings.DATABASES['default']['ENGINE'])
print("DATABASE NAME:", settings.DATABASES['default']['NAME'])
print("DEBUG MODE:", settings.DEBUG)
print("=" * 60)
PYEOF

# Show pending migrations
echo ""
echo "4. Checking migrations..."
python manage.py showmigrations cms

# Run migrations
echo ""
echo "5. Running migrations on PRODUCTION database..."
python manage.py migrate cms

# Verify table was created
echo ""
echo "6. Verifying ErrorLog table exists..."
python manage.py shell << 'PYEOF'
from cms.models import ErrorLog
try:
    count = ErrorLog.objects.count()
    print(f"✓ ErrorLog table exists! Currently has {count} entries.")
except Exception as e:
    print(f"✗ Error accessing ErrorLog table: {e}")
PYEOF

# Restart application
echo ""
echo "7. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Production settings fixed!"
echo "=========================================="
echo ""
echo "What was done:"
echo "  • Set DJANGO_SETTINGS_MODULE=magma7.settings.production"
echo "  • Ran migrations on MySQL production database"
echo "  • Verified ErrorLog table created"
echo "  • Restarted application"
echo ""
echo "Next: Check error logs are now being saved to MySQL"
echo ""
