#!/bin/bash
# Deploy admin fixes to cPanel server

echo "=========================================="
echo "Deploying Admin Fixes"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Show pending migrations
echo ""
echo "2. Checking migrations..."
python manage.py showmigrations cms

# Run migrations
echo ""
echo "3. Running migrations..."
python manage.py migrate cms

# Restart application
echo ""
echo "4. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Admin fixes deployed!"
echo "=========================================="
echo ""
echo "What was fixed:"
echo "  • Added logo_url and favicon_url fields to SiteSettings"
echo "  • Fixed HeroSlides 500 error (by running migrations)"
echo ""
echo "Next steps:"
echo "1. Visit: https://www.magma7fitness.com/admin/"
echo "2. Go to Site Settings - you'll see Logo and Favicon fields"
echo "3. Go to Hero Slides - should work without 500 error"
echo ""
echo "To upload logo/favicon:"
echo "  • Upload images to /home/magmafit/public_html/media/"
echo "  • Then use URL: https://www.magma7fitness.com/media/filename.png"
echo ""
