#!/bin/bash
# Quick script to fix static files issue on cPanel

echo "=========================================="
echo "Fixing Static Files on cPanel"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Collect static files (clear old ones first)
echo ""
echo "2. Collecting static files..."
python manage.py collectstatic --noinput --clear

# Copy to public_html if not using symlink
echo ""
echo "3. Updating public_html/static..."
if [ -L /home/magmafit/public_html/static ]; then
    echo "   Using symlink - no copy needed"
else
    echo "   Copying files..."
    cp -r staticfiles/* /home/magmafit/public_html/static/
fi

# Restart application
echo ""
echo "4. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "✓ Static files updated!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Hard refresh your browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)"
echo "2. Or test in incognito/private window"
echo "3. Visit: https://www.magma7fitness.com/memberships/plans/"
echo ""
echo "If issue persists, the inline CSS fix has been added to the template."
echo ""
