#!/bin/bash
# Deploy Media Center and File Upload features to cPanel server

echo "=========================================="
echo "Deploying Media Center & File Uploads"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

# Activate virtual environment
echo "1. Activating virtual environment..."
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Install Pillow for image processing
echo ""
echo "2. Installing Pillow for image processing..."
pip install Pillow==11.0.0

# Create media directories if they don't exist
echo ""
echo "3. Creating media directories..."
mkdir -p media/media_assets
mkdir -p media/hero_slides
mkdir -p media/branding
chmod 755 media
chmod 755 media/media_assets
chmod 755 media/hero_slides
chmod 755 media/branding

# Create symlink to public_html for media access
echo ""
echo "3b. Creating symlink for media access..."
if [ ! -L ~/public_html/media ]; then
    ln -s /home/magmafit/magma7_proj/media ~/public_html/media
    echo "Symlink created: public_html/media -> magma7_proj/media"
else
    echo "Symlink already exists"
fi

# Show pending migrations
echo ""
echo "4. Checking migrations..."
python manage.py showmigrations cms

# Run migrations
echo ""
echo "5. Running migrations..."
python manage.py migrate cms

# Restart application
echo ""
echo "6. Restarting application..."
touch passenger_wsgi.py

echo ""
echo "=========================================="
echo "Media Center deployed successfully!"
echo "=========================================="
echo ""
echo "What was added:"
echo "  • MediaAsset model - Full media management system"
echo "  • BULK UPLOAD - WordPress-style drag & drop multiple files"
echo "  • File upload support for Hero Slides (image field)"
echo "  • File upload support for Site Settings (logo/favicon)"
echo "  • Image preview in admin"
echo "  • Click-to-copy URLs for uploaded files"
echo ""
echo "Next steps:"
echo "1. Visit: https://www.magma7fitness.com/admin/"
echo "2. Go to 'Media Assets' - Upload and manage all site media"
echo "3. Go to 'Hero Slides' - Now you can upload images directly"
echo "4. Go to 'Site Settings' - Upload logo and favicon files"
echo ""
echo "Media files will be stored in:"
echo "  • /home/magmafit/magma7_proj/media/"
echo "  • Accessible at: https://www.magma7fitness.com/media/"
echo ""
echo "Media Center Features:"
echo "  • BULK UPLOAD - Drag & drop multiple files at once"
echo "  • Upload images, videos, documents"
echo "  • Auto-detect file size and dimensions"
echo "  • Categorize by usage (hero, logo, gallery, etc.)"
echo "  • Click-to-copy URLs"
echo "  • Preview thumbnails in admin list"
echo "  • Full-size preview in edit form"
echo ""
echo "Using Bulk Upload:"
echo "  1. Go to Admin → Media Assets"
echo "  2. Click the '📤 Bulk Upload' button"
echo "  3. Drag & drop multiple files or click to browse"
echo "  4. Files upload automatically with progress indicator"
echo "  5. View results and click links to manage uploaded files"
echo ""
