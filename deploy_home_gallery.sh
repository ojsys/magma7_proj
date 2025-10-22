#!/bin/bash
# Deploy Home Gallery feature to production

echo "=========================================="
echo "Deploy Home Gallery Feature"
echo "=========================================="
echo ""

echo "INSTRUCTIONS:"
echo ""
echo "1. Upload these files to cPanel File Manager:"
echo "   ✓ cms/models.py"
echo "   ✓ cms/admin.py"
echo "   ✓ core/views.py"
echo "   ✓ core/templates/core/home.html"
echo "   ✓ static/css/styles.css"
echo "   ✓ cms/migrations/0009_homegalleryimage.py"
echo ""
echo "2. Then run this script on cPanel Terminal:"
echo ""
echo "   cd /home/magmafit/magma7_proj"
echo "   bash deploy_home_gallery.sh"
echo ""
echo "=========================================="
echo ""
read -p "Have you uploaded all files? (yes/no): " UPLOADED

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

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "Step 1: Checking current migrations..."
python manage.py showmigrations cms | tail -5

echo ""
echo "Step 2: Running migrations..."
python manage.py migrate cms

echo ""
echo "Step 3: Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "Step 4: Restarting application..."
touch passenger_wsgi.py

echo ""
echo "Step 5: Verifying installation..."
python manage.py shell << 'PYEOF'
from cms.models import HomeGalleryImage

print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

try:
    count = HomeGalleryImage.objects.count()
    print(f"✓ HomeGalleryImage table exists")
    print(f"  Gallery images: {count}")
except Exception as e:
    print(f"✗ Error: {e}")

print("="*60 + "\n")
PYEOF

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "What was deployed:"
echo "  ✓ HomeGalleryImage model"
echo "  ✓ Admin interface for gallery management"
echo "  ✓ Homepage gallery section"
echo "  ✓ Gallery CSS styling"
echo ""
echo "Next steps:"
echo "  1. Visit: https://www.magma7fitness.com/admin/cms/homegalleryimage/"
echo "  2. Add facility gallery images"
echo "  3. View on homepage: https://www.magma7fitness.com/"
echo ""
echo "See HOME_GALLERY_GUIDE.md for complete documentation"
echo ""
