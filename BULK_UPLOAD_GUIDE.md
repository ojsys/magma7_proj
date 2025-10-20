# Bulk Upload Guide - WordPress Style

## Quick Start

The Media Center now includes **WordPress-style bulk upload** functionality that lets you upload multiple files at once with drag-and-drop support!

---

## Accessing Bulk Upload

### Option 1: From Media Assets List
1. Go to **Admin → Media Assets**
2. Click the **"📤 Bulk Upload"** button (blue button at top)

### Option 2: Direct URL
Visit: `https://www.magma7fitness.com/cms/admin/bulk-upload/`

---

## How to Use Bulk Upload

### Method 1: Drag & Drop (Recommended)

1. **Open bulk upload page** (see above)
2. **Drag files** from your computer
3. **Drop them** into the upload area
4. Files automatically start uploading
5. View real-time progress bar
6. See upload results with links to each file

### Method 2: Browse and Select

1. Click **"Select Files"** button in the upload area
2. Browse your computer files
3. Select multiple files (hold Ctrl/Cmd to select multiple)
4. Click "Open"
5. Files automatically start uploading

---

## Features

### WordPress-Like Interface
- Clean, modern upload interface
- Large drop zone with visual feedback
- Progress bar with percentage
- Upload summary with statistics
- File-by-file results

### Drag & Drop Support
- Drag files directly from your desktop
- Drop zone highlights when hovering
- Upload multiple files at once
- No file count limit

### Automatic Processing
- **File type detection** - Automatically categorizes as image/video/document
- **File size detection** - Shows human-readable sizes (KB, MB, GB)
- **Image dimensions** - Auto-detects width × height for images
- **Upload tracking** - Records who uploaded each file
- **Metadata** - Timestamps and user information

### Real-Time Feedback
- Progress bar shows upload progress
- Status messages during upload
- Success/error indicators for each file
- Upload summary statistics
- Direct links to view and edit files

### Supported File Types
- **Images**: JPG, JPEG, PNG, GIF, SVG, WebP
- **Videos**: MP4, WebM
- **Documents**: PDF
- **Icons**: ICO

---

## Upload Interface Walkthrough

### Before Upload
```
┌─────────────────────────────────────────┐
│  📤 Bulk Upload Media                   │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │         ☁️                         │ │
│  │  Drop files here to upload        │ │
│  │           or                      │ │
│  │    [Select Files]                 │ │
│  │                                   │ │
│  │  Supported: JPG, PNG, GIF, SVG,  │ │
│  │  WebP, MP4, WebM, PDF, ICO       │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### During Upload
```
┌─────────────────────────────────────────┐
│  Progress                               │
│  ████████████████░░░░░░  75%           │
│  Uploading files...                     │
└─────────────────────────────────────────┘
```

### After Upload
```
┌─────────────────────────────────────────┐
│  ✓ Upload Complete                      │
│  5 files uploaded successfully          │
│                                         │
│  🖼️ hero-image.jpg                      │
│      image • 1.2 MB • 1920×1080        │
│      View file | Edit in admin          │
│      ✓ Uploaded                         │
│                                         │
│  🖼️ logo.png                            │
│      image • 156 KB • 400×120          │
│      View file | Edit in admin          │
│      ✓ Uploaded                         │
│                                         │
│  [Upload More Files]  [← Back]         │
└─────────────────────────────────────────┘
```

---

## Upload Results

After uploading, you'll see detailed results for each file:

### Successful Upload
```
🖼️ my-image.jpg
   image • 2.3 MB • 2400×1600
   View file | Edit in admin
   ✓ Uploaded
```

Shows:
- File icon (based on type)
- Filename
- File type, size, and dimensions
- Links to view the file or edit in admin
- Success indicator

### Failed Upload
```
📎 broken-file.xyz
   Invalid file type
   ✗ Failed
```

Shows:
- File icon
- Filename
- Error message
- Failed indicator

---

## Comparison: Single vs Bulk Upload

### Single Upload (Traditional)
```
1. Click "Add Media Asset"
2. Fill in form
3. Choose file
4. Fill in details (title, description, etc.)
5. Click "Save"
6. Repeat for each file
```
**Time for 10 files**: ~5 minutes

### Bulk Upload (New!)
```
1. Click "Bulk Upload"
2. Drag & drop all files
3. Done!
```
**Time for 10 files**: ~30 seconds

**Benefits:**
- 90% faster for multiple files
- Auto-detects file types and metadata
- Shows progress for all files
- No need to fill individual forms
- Can edit details later if needed

---

## After Bulk Upload

### View Uploaded Files
1. Click **"Back to Media Library"** button
2. Or click **"Edit in admin"** link for specific file
3. All uploaded files appear in the Media Assets list

### Edit File Details
Files are uploaded with basic information. To add more details:

1. Go to **Admin → Media Assets**
2. Find your uploaded file (use search if needed)
3. Click to edit
4. Add:
   - Better title (auto-set to filename)
   - Description
   - Usage category (hero, logo, gallery, etc.)
   - Alt text (for accessibility)
5. Click "Save"

### Get File URLs
After upload, each file result has a **"View file"** link that opens the file URL. Or:

1. Click **"Edit in admin"** link
2. In the edit form, click the **"File URL"** field
3. URL automatically copies to clipboard
4. Use in your templates or content

---

## Tips for Efficient Bulk Upload

### Before Uploading
1. **Organize files** - Put all files to upload in one folder
2. **Name files** - Use descriptive names (hero-home.jpg, not IMG_1234.jpg)
3. **Optimize images** - Compress large images before upload (TinyPNG, etc.)
4. **Check formats** - Ensure files are in supported formats

### During Upload
1. **Stable connection** - Ensure good internet connection
2. **Don't close page** - Stay on page until upload completes
3. **Large files** - Upload very large files separately if needed

### After Upload
1. **Review results** - Check that all files uploaded successfully
2. **Edit metadata** - Add descriptions and alt text for images
3. **Categorize** - Set usage category for easier finding later
4. **Test files** - Click "View file" to verify files are accessible

---

## Use Cases

### 1. New Website Setup
Upload all site images at once:
- Hero slides (5-10 images)
- Logo and favicon
- Team photos (10-20 images)
- Facility photos (20-30 images)
- Service images

**Total**: 50+ images in one bulk upload!

### 2. Blog Post with Multiple Images
Upload all images for a new blog post or article at once.

### 3. Gallery Update
Add multiple new photos to a gallery in one go.

### 4. Seasonal Content
Update hero slides and promotional images for new season/promotion.

### 5. Team Updates
Add new team member photos when multiple people join.

---

## Troubleshooting

### Upload Fails Completely

**"No files provided" error:**
- Make sure you dropped files in the drop zone
- Or selected files with the file picker
- Try refreshing the page and uploading again

**Network error:**
- Check your internet connection
- Try uploading fewer files at once
- Check server is accessible

### Some Files Fail

Files that fail will show error messages:

**"Invalid file type":**
- File extension not in supported list
- Convert to supported format (JPG, PNG, etc.)

**"File too large":**
- Check server upload limits in cPanel
- Compress image before uploading
- Upload file individually with compression

**Permission errors:**
- Contact server administrator
- Check media directory permissions (should be 755)

### Files Upload but Don't Appear

**Check migration ran:**
```bash
python manage.py showmigrations cms
# Should show [X] 0003_add_media_center_and_file_uploads
```

**Check media directory exists:**
```bash
ls -la /home/magmafit/magma7_proj/media/
```

**Restart application:**
```bash
touch /home/magmafit/magma7_proj/passenger_wsgi.py
```

---

## Technical Details

### How It Works

1. **Frontend**: Drag & drop interface using HTML5 File API
2. **AJAX Upload**: Files sent via FormData to backend
3. **Django Processing**: Each file processed server-side
4. **Metadata Extraction**: Auto-detect type, size, dimensions
5. **Database Save**: Create MediaAsset records
6. **Response**: Return JSON with results
7. **Display Results**: Show success/error for each file

### File Storage

Files are stored in:
```
/home/magmafit/magma7_proj/media/media_assets/2025/01/
```

Organized by year and month for easy management.

### Security

- Only admin users can access bulk upload
- File type validation on backend
- File extension whitelist enforced
- CSRF token required for upload
- Files uploaded with unique names to prevent overwriting

---

## Best Practices

### File Naming
- Use descriptive names: `hero-fitness-class.jpg`
- Use hyphens, not spaces: `team-member-john.jpg`
- Include context: `facility-gym-floor.jpg`
- Avoid generic names: `image1.jpg`

### Image Optimization
Before bulk upload, optimize images:
- **Hero slides**: Max 1920×1080, under 500KB
- **Logos**: Max 400×120, under 200KB
- **Photos**: Max 2000px width, under 500KB
- **Icons/favicons**: Max 64×64, under 50KB

**Tools**: TinyPNG, ImageOptim, Squoosh

### Organization
After bulk upload:
- Set **Usage** category for each file
- Add **Alt text** for images (accessibility)
- Add **Description** for better search
- Mark inactive if not currently used

---

## Comparison with WordPress

Features matching WordPress Media Library:

| Feature | WordPress | Magma7 Media Center |
|---------|-----------|---------------------|
| Bulk Upload | ✅ Yes | ✅ Yes |
| Drag & Drop | ✅ Yes | ✅ Yes |
| Progress Bar | ✅ Yes | ✅ Yes |
| Auto Metadata | ✅ Yes | ✅ Yes |
| File Preview | ✅ Yes | ✅ Yes |
| Grid View | ✅ Yes | ✅ Yes (list with thumbnails) |
| Search | ✅ Yes | ✅ Yes |
| Filters | ✅ Yes | ✅ Yes |
| Click-to-Copy URL | ❌ No | ✅ Yes (Better!) |
| Usage Categories | ❌ Limited | ✅ Yes (More detailed) |

---

## Summary

The bulk upload feature makes managing media as easy as WordPress:

1. **Fast** - Upload dozens of files in seconds
2. **Easy** - Just drag & drop, no forms to fill
3. **Smart** - Auto-detects file types and metadata
4. **Visual** - See progress and results in real-time
5. **Reliable** - Individual file error handling

**No more uploading files one by one!**

---

## Quick Reference Commands

**Access bulk upload:**
```
Admin → Media Assets → 📤 Bulk Upload
```

**Direct URL:**
```
https://www.magma7fitness.com/cms/admin/bulk-upload/
```

**Upload files:**
```
Drag & drop OR Click "Select Files"
```

**After upload:**
```
Click "Back to Media Library" or "Edit in admin"
```

---

Enjoy the WordPress-style bulk upload experience!
