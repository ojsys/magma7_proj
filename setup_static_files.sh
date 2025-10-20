#!/bin/bash
# Script to set up static files for Django on cPanel

echo "=========================================="
echo "Setting up Static Files for Magma7Fitness"
echo "=========================================="
echo ""

# Change to project directory
cd /home/magmafit/magma7_proj || exit

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set Django settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Collect static files
echo ""
echo "2. Collecting static files..."
python manage.py collectstatic --noinput

# Create media directory if it doesn't exist
echo ""
echo "3. Creating media directory..."
mkdir -p /home/magmafit/magma7_proj/media

# Remove old links/directories if they exist
echo ""
echo "4. Setting up public_html links..."
rm -rf /home/magmafit/public_html/static
rm -rf /home/magmafit/public_html/media

# Try creating symbolic links
echo "   Creating symbolic links..."
if ln -s /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static 2>/dev/null; then
    echo "   ✓ Static files symlink created"
else
    echo "   ✗ Symlinks not supported, copying files instead..."
    cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
    echo "   ✓ Static files copied"
fi

if ln -s /home/magmafit/magma7_proj/media /home/magmafit/public_html/media 2>/dev/null; then
    echo "   ✓ Media files symlink created"
else
    echo "   ✗ Symlinks not supported, copying directory instead..."
    cp -r /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
    echo "   ✓ Media directory copied"
fi

# Set permissions
echo ""
echo "5. Setting file permissions..."
chmod 755 /home/magmafit/public_html/static
chmod 755 /home/magmafit/public_html/media
find /home/magmafit/public_html/static -type d -exec chmod 755 {} \;
find /home/magmafit/public_html/static -type f -exec chmod 644 {} \;

# Restart application
echo ""
echo "6. Restarting application..."
touch /home/magmafit/magma7_proj/passenger_wsgi.py

echo ""
echo "=========================================="
echo "Static files setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Visit your website: https://www.magma7fitness.com"
echo "2. Check if styles are loading"
echo "3. Test admin panel: https://www.magma7fitness.com/admin"
echo ""
echo "If styles still don't load:"
echo "- Configure static files in cPanel Python App"
echo "- Add: URL=/static/ Path=/home/magmafit/public_html/static"
echo ""
