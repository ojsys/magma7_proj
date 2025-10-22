# Home Gallery Feature - Complete Guide

## Overview

A beautiful image gallery section has been added to the homepage showcasing your facility. Admin users can easily manage the gallery images from the Django admin panel.

---

## Features

✅ **Admin-Managed Gallery** - Add, edit, remove, and reorder images from admin panel
✅ **Responsive Grid Layout** - Automatically adjusts to any screen size
✅ **Hover Effects** - Beautiful overlay with title and description on hover
✅ **Image Preview** - See thumbnails in admin list view
✅ **Order Control** - Set display order with drag-and-drop style ordering
✅ **Active/Inactive Toggle** - Show or hide images without deleting them
✅ **Media Center Integration** - Use images from your Media Center
✅ **Loading Optimization** - Lazy loading for better performance

---

## Location on Homepage

The gallery appears **after the "Why Choose Magma7Fitness" section** and **before the pricing plans**.

Section order:
1. Hero
2. Programs
3. Why Choose Us
4. **→ Facility Gallery (NEW)** ←
5. Pricing Plans
6. Testimonials

---

## How to Add Gallery Images

### Step 1: Upload Images to Media Center

1. Go to Django Admin: `/admin/`
2. Navigate to: **CMS → Media Assets**
3. Click **"📤 Bulk Upload"** button (top right)
4. Drag and drop your facility photos
5. Once uploaded, **copy the image URL** (click to copy)

### Step 2: Add to Home Gallery

1. In Django Admin, go to: **CMS → Home Gallery Images**
2. Click **"Add Home Gallery Image"**
3. Fill in the form:
   - **Image URL:** Paste the URL from Media Center
   - **Title:** e.g., "Cardio Zone", "Free Weights Area"
   - **Description:** Brief description shown on hover (optional)
   - **Order:** Lower numbers appear first (0, 1, 2, 3...)
   - **Is active:** Check to show on homepage
4. Click **"Save"**

### Step 3: Verify on Homepage

Visit your homepage: The gallery should appear with all active images.

---

## Managing Gallery Images

### View All Images

**Admin → CMS → Home Gallery Images**

You'll see a list with:
- Thumbnail preview
- Title
- Order number (editable in list)
- Active status (toggle in list)

### Reorder Images

Click on the **Order** number in the list and change it:
- Order 0 = First image
- Order 1 = Second image
- Order 2 = Third image
- etc.

Click **"Save"** at the bottom to apply changes.

### Edit an Image

1. Click on the image title in the list
2. Update any field
3. Large preview shows at bottom
4. Click **"Save"**

### Hide an Image (Without Deleting)

In the list view, **uncheck** the checkbox under "Is active" for that image.
The image stays in the database but won't show on the homepage.

### Delete an Image

1. Check the box next to the image(s) you want to delete
2. Select **"Delete selected Home Gallery Images"** from the dropdown
3. Click **"Go"**
4. Confirm deletion

---

## Best Practices

### Image Specifications

**Recommended Size:**
- **Width:** 800-1200px
- **Height:** 600-900px
- **Aspect Ratio:** 4:3 or 16:9
- **Format:** JPG or PNG
- **File Size:** < 500KB (for fast loading)

### Image Content Suggestions

Good subjects for facility gallery:
- Gym floor with equipment
- Cardio machines area
- Free weights section
- Group fitness studio
- Locker rooms
- Reception/lobby
- Personal training areas
- Stretching zones
- Functional training area
- Outdoor training space (if applicable)

### How Many Images?

**Recommended:** 6-8 images
- Enough to showcase variety
- Not overwhelming for visitors
- Loads quickly

**Minimum:** 3 images
**Maximum:** 12 images (beyond this, consider a dedicated gallery page)

### Ordering Strategy

**Suggested order:**
1. **Most impressive space first** - Main gym floor or signature area
2. **Cardio zone** - Show the variety of cardio equipment
3. **Strength training** - Free weights, machines
4. **Functional training** - Unique features
5. **Group fitness** - Studio, classes
6. **Amenities** - Locker rooms, reception

---

## Example Setup

```python
# Example images to add:

Image 1:
  Title: "Main Gym Floor"
  Description: "Over 10,000 sq ft of premium training space"
  Order: 0

Image 2:
  Title: "Cardio Zone"
  Description: "Latest treadmills, bikes, and ellipticals"
  Order: 1

Image 3:
  Title: "Free Weights Area"
  Description: "Complete range of dumbbells and barbells"
  Order: 2

Image 4:
  Title: "Functional Training"
  Description: "Battle ropes, kettlebells, and TRX systems"
  Order: 3

Image 5:
  Title: "Group Fitness Studio"
  Description: "Spacious studio for yoga, spin, and group classes"
  Order: 4

Image 6:
  Title: "Personal Training Zone"
  Description: "Dedicated area for one-on-one sessions"
  Order: 5
```

---

## Visual Appearance

### Desktop View (Large Screens)
- **Grid:** 3-4 columns
- **Hover Effect:** Image zooms slightly, overlay fades in
- **Overlay:** Dark green gradient from bottom
- **Text:** White title and description
- **Animation:** Smooth transitions

### Tablet View (Medium Screens)
- **Grid:** 2-3 columns
- **Same effects** as desktop

### Mobile View (Small Screens)
- **Grid:** 1 column (stacked)
- **Tap to reveal** overlay
- **Optimized spacing**

---

## Gallery Controls

### Show/Hide Entire Gallery

The gallery only shows if there are **active images**.

To hide the entire section:
1. Go to **Home Gallery Images** in admin
2. Uncheck **"Is active"** for all images
3. Gallery section disappears from homepage

To show again:
- Check **"Is active"** for at least one image

### Link to Facilities Page

At the bottom of the gallery, there's a button:
**"Explore All Facilities"** → Links to `/facilities/`

You can customize this in the template if needed.

---

## Troubleshooting

### Gallery not showing on homepage

**Check:**
1. Is at least one image marked **"Is active"** ✓
2. Does the image have a valid **Image URL** ✓
3. Did you refresh the page after adding images ✓

### Image not loading

**Check:**
1. Copy/paste the image URL into browser - does it load?
2. Check for typos in the URL
3. Make sure the image is uploaded to Media Center
4. Check file permissions on the server

### Images in wrong order

**Fix:**
1. Go to Home Gallery Images list
2. Click on the **Order** number
3. Change to desired order (0, 1, 2, 3...)
4. Save

### Overlay not showing on hover

**Check:**
- CSS is loading properly
- Browser cache (try hard refresh: Ctrl+F5 / Cmd+Shift+R)
- No JavaScript errors in console

---

## Advanced Customization

### Change Gallery Title

Edit `core/templates/core/home.html`, line ~130:

```html
<h2>Our State-of-the-Art Facility</h2>
```

Change to your preferred title.

### Change Gallery Description

Edit line ~131:

```html
<p style="color: var(--text-secondary); font-size: 1.1rem;">
  Explore our premium fitness center equipped with the latest equipment and amenities
</p>
```

### Change Number of Images Shown

Edit `core/views.py`, line ~20:

```python
gallery_images = HomeGalleryImage.objects.filter(is_active=True).order_by('order')[:8]
```

Change `[:8]` to `[:12]` for 12 images, or remove `[:8]` to show all.

### Change Grid Columns

Edit `static/css/styles.css`, find `.facility-gallery`:

```css
.facility-gallery {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
```

Change `280px` to:
- `350px` = fewer, larger images
- `200px` = more, smaller images

---

## Technical Details

### Database Model

**Table:** `cms_homegalleryimage`

**Fields:**
- `id` - Auto-increment primary key
- `title` - VARCHAR(150)
- `image_url` - VARCHAR(200)
- `description` - TEXT
- `order` - INTEGER
- `is_active` - BOOLEAN

### Admin Interface

**Location:** `/admin/cms/homegalleryimage/`

**Permissions:**
- Staff users can view/edit
- Superusers can add/delete

**Features:**
- List view with thumbnails
- Inline editing for order and active status
- Large preview in edit form
- Search by title or description
- Filter by active status

### Frontend Template

**File:** `core/templates/core/home.html`
**Lines:** ~124-165

Uses Django template tags:
- `{% for img in gallery_images %}`
- `{{ img.image_url }}`
- `{{ img.title }}`
- `{{ img.description }}`

### CSS Styles

**File:** `static/css/styles.css`
**Section:** Facility Gallery Section

Key classes:
- `.facility-gallery` - Grid container
- `.gallery-item` - Individual image container
- `.gallery-overlay` - Hover overlay
- `.gallery-content` - Title and description

---

## Migration

**File:** `cms/migrations/0009_homegalleryimage.py`

Creates the `HomeGalleryImage` table with all fields and indexes.

**To apply on production:**
```bash
python manage.py migrate cms
```

---

## Quick Start Checklist

- [ ] Run migration: `python manage.py migrate cms`
- [ ] Upload 6-8 facility photos to Media Center
- [ ] Go to Home Gallery Images in admin
- [ ] Add images with titles and descriptions
- [ ] Set order numbers (0, 1, 2, 3, 4, 5...)
- [ ] Mark all as "Is active"
- [ ] Visit homepage to verify gallery appears
- [ ] Test hover effects on desktop
- [ ] Test on mobile device
- [ ] Adjust image order if needed

---

## Support

**Admin Panel:** `/admin/cms/homegalleryimage/`
**Media Center:** `/admin/cms/mediaasset/`
**Bulk Upload:** `/admin/cms/mediaasset/` → "📤 Bulk Upload" button

---

**Status:** Ready to use! ✓

**Created:** 2025-10-22
