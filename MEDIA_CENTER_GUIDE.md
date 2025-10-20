# Media Center & File Upload Guide

## Overview

The Media Center provides centralized management of all site media assets with easy file uploads. You can now upload images, videos, and documents directly through the Django admin instead of using external URLs.

---

## What's New

### 1. Media Center (Media Assets)
- Upload and manage all site media in one place
- Automatic file size and dimension detection
- Categorize by usage (hero, logo, gallery, etc.)
- Click-to-copy URLs for easy reference
- Preview thumbnails and full-size images
- Track who uploaded each file and when

### 2. Hero Slides - File Upload
- Upload hero slide images directly
- Still supports external URLs as fallback
- Preview images in admin list and edit form
- Uploaded files take priority over URLs

### 3. Site Settings - Logo & Favicon Upload
- Upload logo and favicon files directly
- Still supports external URLs as fallback
- Live preview of logo and favicon in admin
- Recommended formats and sizes displayed

---

## Deployment to cPanel

### Step 1: Upload Updated Files

Upload these files to your server:

```bash
# From your local machine
scp cms/models.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/
scp cms/admin.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/
scp cms/migrations/0003_add_media_center_and_file_uploads.py magmafit@yourserver:/home/magmafit/magma7_proj/cms/migrations/
scp requirements.txt magmafit@yourserver:/home/magmafit/magma7_proj/
```

Or use the deployment script:

```bash
scp deploy_media_center.sh magmafit@yourserver:/home/magmafit/
```

### Step 2: Run Deployment Script

SSH into your server and run:

```bash
ssh magmafit@yourserver
chmod +x deploy_media_center.sh
./deploy_media_center.sh
```

The script will:
1. Activate virtual environment
2. Install Pillow (image processing library)
3. Create media directories with correct permissions
4. Run database migrations
5. Restart the application

### Step 3: Manual Deployment (Alternative)

If you prefer manual steps:

```bash
ssh magmafit@yourserver
cd /home/magmafit/magma7_proj

# Activate virtual environment
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Install Pillow
pip install Pillow==11.0.0

# Create media directories
mkdir -p media/media_assets media/hero_slides media/branding
chmod 755 media media/media_assets media/hero_slides media/branding

# Run migrations
python manage.py migrate cms

# Restart application
touch passenger_wsgi.py
```

### Step 4: Configure Media File Serving

Ensure your Apache/cPanel is configured to serve media files. Add to `.htaccess` if needed:

```apache
# Serve media files
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_URI} ^/media/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

---

## Using the Media Center

### Access Media Center

1. Visit: `https://www.magma7fitness.com/admin/`
2. Click **"Media Assets"** in the CMS section
3. Click **"Add Media Asset"** to upload new files

### Upload a Media Asset

**Step 1: Upload File**
- Click "Choose File" under "File"
- Select your image/video/document
- Supported formats:
  - Images: JPG, PNG, GIF, SVG, WebP
  - Videos: MP4, WebM
  - Documents: PDF
  - Icons: ICO

**Step 2: Fill in Details**
- **Title**: Descriptive name (e.g., "Homepage Hero Image")
- **Description**: Optional details about the file
- **Asset Type**: Image, Video, Document, or Other (auto-detected)
- **Usage**: Categorize by use:
  - Hero Slide
  - Logo/Branding
  - Service Image
  - Team Photo
  - Facility Photo
  - Gallery
  - General Use
- **Alt Text**: For accessibility (important for images)

**Step 3: Save**
- Click "Save" or "Save and continue editing"
- File is automatically processed:
  - File size calculated
  - Image dimensions detected (width × height)
  - URL generated

**Step 4: Copy URL**
- In the edit form, you'll see a "File URL" field
- Click the input field to auto-copy the URL
- Use this URL anywhere in your site

### Using Uploaded Media

**Get the URL:**
1. Go to Media Assets
2. Find your file
3. Click to edit
4. Click the "File URL" field to copy

**Use in templates:**
```html
<img src="https://www.magma7fitness.com/media/media_assets/2025/01/hero-image.jpg" alt="Hero">
```

---

## Hero Slides with File Upload

### Option 1: Upload File Directly

1. Go to **Admin → Hero Slides**
2. Click **"Add Hero Slide"** or edit existing slide
3. Under "Slide Image":
   - Click **"Choose File"** under "Image"
   - Select your image file
   - Preview will appear after save
4. Fill in **Title**
5. Set **Order** and **Is Active**
6. Click **"Save"**

**Recommended image size**: 1920×1080px or larger

### Option 2: Use External URL (Fallback)

1. Leave "Image" field empty
2. Fill in "Image url" with external URL
3. This is useful for:
   - Images hosted on CDN
   - Temporary testing
   - Very large files

**Priority**: If both "Image" and "Image url" are provided, the uploaded file takes priority.

### Preview in Admin

- **List View**: Shows 80×50px thumbnail
- **Edit Form**: Shows large preview (max 600×300px)
- If no image: Shows "No image uploaded or URL provided yet"

---

## Logo & Favicon with File Upload

### Upload Logo

1. Go to **Admin → Site Settings**
2. Under "Branding" section:
   - Click **"Choose File"** under "Logo"
   - Select your logo file
   - Preview appears below
3. Leave "Logo url" empty (or keep as fallback)
4. Click **"Save"**

**Recommended logo specs:**
- Format: PNG with transparent background (or SVG)
- Size: 200×60 pixels (or similar ratio)
- Max file size: 500KB

### Upload Favicon

1. In the same "Branding" section:
   - Click **"Choose File"** under "Favicon"
   - Select your favicon file
   - Preview appears below (32×32px)
2. Leave "Favicon url" empty (or keep as fallback)
3. Click **"Save"**

**Recommended favicon specs:**
- Format: ICO or PNG
- Size: 32×32 or 64×64 pixels
- Max file size: 50KB

### Priority System

Both logo and favicon support dual mode:
- **Uploaded file takes priority** if present
- Falls back to URL if no file uploaded
- This allows gradual migration from URLs to uploads

---

## Templates Using Uploaded Files

The `get_logo_url()`, `get_favicon_url()`, and `get_image_url()` methods automatically return the correct URL (uploaded file or fallback URL).

### Update Your Templates

**Logo:**
```html
{% if site_settings.logo or site_settings.logo_url %}
<img src="{{ site_settings.get_logo_url }}" alt="{{ site_settings.brand_name }}">
{% else %}
{{ site_settings.brand_name }}
{% endif %}
```

**Favicon:**
```html
{% if site_settings.favicon or site_settings.favicon_url %}
<link rel="icon" type="image/x-icon" href="{{ site_settings.get_favicon_url }}">
{% endif %}
```

**Hero Slides:**
```html
{% for slide in hero_slides %}
<div class="slide">
  <img src="{{ slide.get_image_url }}" alt="{{ slide.title }}">
  <h2>{{ slide.title }}</h2>
</div>
{% endfor %}
```

---

## File Organization

Uploaded files are automatically organized by type and date:

```
/home/magmafit/magma7_proj/media/
├── media_assets/
│   ├── 2025/
│   │   ├── 01/           # January 2025 uploads
│   │   │   ├── image1.jpg
│   │   │   └── image2.png
│   │   └── 02/           # February 2025 uploads
│   └── ...
├── hero_slides/
│   ├── slide1.jpg
│   ├── slide2.jpg
│   └── ...
└── branding/
    ├── logo.png
    └── favicon.ico
```

**Media URLs:**
- Base: `https://www.magma7fitness.com/media/`
- Media Assets: `https://www.magma7fitness.com/media/media_assets/2025/01/image.jpg`
- Hero Slides: `https://www.magma7fitness.com/media/hero_slides/slide.jpg`
- Branding: `https://www.magma7fitness.com/media/branding/logo.png`

---

## Admin Features

### Media Assets Admin

**List View Columns:**
- Thumbnail Preview (50×50px)
- Title
- Asset Type (Image/Video/Document)
- Usage Category
- File Size (human-readable: KB/MB/GB)
- Dimensions (width × height for images)
- Created Date
- Is Active

**Filters:**
- Asset Type
- Usage Category
- Is Active
- Created Date

**Search:**
- Title
- Description
- Alt Text

**Edit Form:**
- Upload File section with large preview
- Asset Information (title, description, type, usage, alt text)
- File Details (collapsible: URL, size, dimensions)
- Metadata (collapsible: uploader, active status, timestamps)

**Features:**
- Click-to-copy URL with alert confirmation
- Auto-detect file size
- Auto-detect image dimensions
- Auto-set uploaded_by to current user
- Readonly fields for metadata

### Hero Slides Admin

**List View:**
- Title
- Image Preview (80×50px)
- Order
- Is Active
- Created Date

**Edit Form:**
- Slide Image section:
  - Upload image file
  - Large preview (max 600×300px)
  - OR provide external URL
- Slide Information (title)
- Display Settings (active, order)

### Site Settings Admin

**Branding Section:**
- Brand Name
- Tagline
- **Logo** (upload file)
- Logo Preview (max 60px height)
- Logo url (fallback)
- **Favicon** (upload file)
- Favicon Preview (32×32px)
- Favicon url (fallback)

---

## Troubleshooting

### Media Files Not Accessible

**Check directory permissions:**
```bash
ls -la /home/magmafit/magma7_proj/media/
# Should show: drwxr-xr-x (755)

chmod 755 /home/magmafit/magma7_proj/media/
chmod 755 /home/magmafit/magma7_proj/media/media_assets/
chmod 755 /home/magmafit/magma7_proj/media/hero_slides/
chmod 755 /home/magmafit/magma7_proj/media/branding/
```

**Check file permissions:**
```bash
ls -la /home/magmafit/magma7_proj/media/branding/
# Files should be readable (644 or 755)

chmod 644 /home/magmafit/magma7_proj/media/branding/*.png
chmod 644 /home/magmafit/magma7_proj/media/branding/*.ico
```

**Check .htaccess media serving:**
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_URI} ^/media/ [NC]
    RewriteRule ^(.*)$ - [L]
</IfModule>
```

### Upload Errors

**"No module named 'PIL'":**
```bash
pip install Pillow==11.0.0
touch passenger_wsgi.py
```

**"Permission denied" when uploading:**
```bash
# Check media directory ownership
ls -la /home/magmafit/magma7_proj/

# Ensure directory is writable
chmod 755 /home/magmafit/magma7_proj/media/
```

**"File too large":**
- Check your server's upload limits in cPanel
- PHP settings: `upload_max_filesize` and `post_max_size`
- Passenger/Apache settings

### Images Not Showing in Admin

**Pillow not installed:**
```bash
source ~/virtualenv/magma7_proj/3.12/bin/activate
pip install Pillow==11.0.0
touch passenger_wsgi.py
```

**MEDIA_URL not configured:**
```python
# In magma7/settings/base.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Migration not run:**
```bash
python manage.py showmigrations cms
python manage.py migrate cms
```

---

## Best Practices

### File Naming
- Use descriptive names: `hero-home-fitness.jpg` not `image123.jpg`
- Avoid spaces: Use hyphens or underscores
- Lowercase preferred: `logo-magma7.png`

### Image Optimization
- Compress images before upload (TinyPNG, ImageOptim)
- Use appropriate formats:
  - Photos: JPG
  - Graphics/logos: PNG
  - Icons: SVG or PNG
  - Favicons: ICO or PNG
- Recommended max file sizes:
  - Hero images: 500KB
  - Logos: 200KB
  - Icons: 50KB

### Alt Text
- Always provide alt text for images (accessibility)
- Describe what's in the image
- Keep under 125 characters
- Don't start with "Image of..." (screen readers know it's an image)

### Organization
- Use Usage categories consistently
- Delete unused files regularly
- Deactivate instead of delete if might be needed later

### Security
- Only upload trusted files
- Don't upload executable files
- Be cautious with SVG files (can contain scripts)
- Review uploaded files periodically

---

## Migration from URLs to Uploads

If you have existing content using URLs, you can gradually migrate:

1. **Keep existing URLs working** - The dual system supports both
2. **Upload new files** - Use uploads for new content
3. **Replace URLs gradually**:
   - Download images from current URLs
   - Upload to Media Center
   - Copy new URLs
   - Update templates
4. **Test thoroughly** before removing old URLs

---

## Success Criteria

After deployment, verify:

**Media Center:**
- [ ] "Media Assets" appears in admin
- [ ] Can upload image files
- [ ] Preview shows in edit form
- [ ] File URL is clickable and copyable
- [ ] File size shows correctly
- [ ] Image dimensions show correctly
- [ ] Uploaded files accessible at URL

**Hero Slides:**
- [ ] "Image" upload field appears
- [ ] Can upload hero slide images
- [ ] Preview shows in admin list
- [ ] Large preview shows in edit form
- [ ] Uploaded image displays on frontend

**Site Settings:**
- [ ] "Logo" and "Favicon" upload fields appear
- [ ] Can upload logo file
- [ ] Can upload favicon file
- [ ] Previews show in admin
- [ ] Logo displays on frontend
- [ ] Favicon displays in browser tab

---

## Quick Reference

### Upload Logo
Admin → Site Settings → Branding → Logo (choose file) → Save

### Upload Favicon
Admin → Site Settings → Branding → Favicon (choose file) → Save

### Upload Hero Slide
Admin → Hero Slides → Add Hero Slide → Image (choose file) → Title → Save

### Upload Media Asset
Admin → Media Assets → Add Media Asset → File (choose file) → Fill details → Save

### Get Media URL
Admin → Media Assets → (click asset) → Click "File URL" field → URL copied!

---

## Need Help?

**Check logs:**
```bash
tail -50 /home/magmafit/magma7_proj/logs/django_errors.log
```

**Test media serving:**
```bash
curl -I https://www.magma7fitness.com/media/test.jpg
# Should return 200 OK
```

**Verify migrations:**
```bash
python manage.py showmigrations cms
# Should show [X] 0003_add_media_center_and_file_uploads
```

**Database shell test:**
```bash
python manage.py shell
```
```python
from cms.models import MediaAsset
print(MediaAsset.objects.count())
# Should work without errors
```

---

## Summary

The Media Center provides:
- Centralized media management
- Easy file uploads with drag-and-drop
- Automatic file processing (size, dimensions)
- Click-to-copy URLs
- Preview in admin
- Backward compatibility with URLs
- Organized file storage by date
- Track upload history

You now have complete control over site media without needing external hosting services!
