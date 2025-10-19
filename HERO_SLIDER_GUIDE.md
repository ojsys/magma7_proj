# Hero Slider Setup Guide

## Overview

The home page hero section now features a dynamic background image slider that can be fully managed from the Django admin panel. The slider automatically rotates through multiple high-quality images with smooth transitions.

## Features

✅ **Admin-Managed**: Add, edit, and reorder slides from the admin panel
✅ **Automatic Rotation**: Slides change every 5 seconds automatically
✅ **Manual Navigation**: Click dots to jump to specific slides
✅ **Keyboard Support**: Use arrow keys to navigate (left/right)
✅ **Touch/Swipe Support**: Swipe on mobile devices to change slides
✅ **Pause on Hover**: Automatic rotation pauses when hovering over the hero
✅ **Smooth Transitions**: 1.5 second fade transitions between slides
✅ **Responsive**: Works perfectly on all device sizes
✅ **Fallback**: Shows placeholder image if no slides are configured

## How to Add/Manage Hero Slides

### Step 1: Access the Admin Panel

1. Navigate to: `http://yourdomain.com/admin/`
2. Log in with your admin credentials
3. Look for **"CMS"** section in the sidebar
4. Click on **"Hero Slides"**

### Step 2: Add a New Slide

1. Click the **"Add Hero Slide"** button
2. Fill in the following fields:

   **Title**
   - A descriptive name for the slide (for admin reference only)
   - Example: "Gym Equipment Background", "Training Session", "Fitness Class"

   **Image URL**
   - The URL of the background image
   - Recommended size: Minimum 1920x1080 pixels
   - Use high-quality images for best results
   - Supported formats: JPG, PNG, WebP

   **Is Active**
   - Check this box to show the slide in rotation
   - Uncheck to temporarily hide the slide without deleting it

   **Order**
   - Controls the display order (lower numbers show first)
   - Example: Order 0 shows before Order 1
   - Slides rotate in this order

3. Click **"Save"** to add the slide

### Step 3: Manage Existing Slides

**Edit a Slide**:
- Click on the slide title in the list
- Update any fields as needed
- Click "Save"

**Reorder Slides**:
- Change the "Order" number in the list view
- Lower numbers display first
- Changes are applied immediately

**Deactivate a Slide**:
- Uncheck "Is Active" in the list view
- The slide will be hidden but not deleted

**Delete a Slide**:
- Select the slide(s) using checkboxes
- Choose "Delete selected hero slides" from the actions dropdown
- Click "Go"

## Recommended Image Specifications

### Image Dimensions
- **Minimum Resolution**: 1920x1080 pixels (Full HD)
- **Recommended**: 2560x1440 pixels or higher
- **Aspect Ratio**: 16:9 (widescreen)

### Image Quality
- Use high-quality, professionally-shot images
- Ensure good lighting and clear subjects
- Avoid cluttered or busy backgrounds
- Consider how text will overlay the image

### File Format
- **Best**: JPG (for photographs)
- **Alternative**: PNG (for graphics with transparency needs)
- **Modern**: WebP (smaller file size, excellent quality)

### Image Optimization
- Compress images before uploading to reduce load time
- Use tools like TinyPNG, ImageOptim, or Squoosh
- Target file size: Under 500KB per image

### Image Sources
- **Unsplash**: https://unsplash.com (free high-quality photos)
- **Pexels**: https://pexels.com (free stock photos)
- **Your Own Photos**: Professional gym photography

## Example Image URLs

Here are some example fitness-themed images you can use:

```
Gym Equipment:
https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2000&auto=format&fit=crop

Personal Training:
https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2000&auto=format&fit=crop

Group Fitness Class:
https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=2000&auto=format&fit=crop

Cardio Equipment:
https://images.unsplash.com/photo-1571902943202-507ec2618e8f?q=80&w=2000&auto=format&fit=crop

Weight Training:
https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop
```

## Technical Details

### Slider Behavior

**Automatic Rotation**:
- Default interval: 5 seconds per slide
- Pauses when user hovers over hero section
- Pauses when browser tab is not visible
- Resumes when tab becomes active again

**Manual Controls**:
- **Dots**: Click any dot to jump to that slide
- **Keyboard**: Use ← → arrow keys to navigate
- **Touch**: Swipe left/right on mobile devices

**Transitions**:
- Smooth fade effect (1.5 seconds)
- CSS-based animations for best performance
- No jarring jumps between slides

### Fallback Behavior

If no slides are configured in the admin:
- A default placeholder image is shown
- Hero section remains fully functional
- No errors or broken layouts

### Performance

**Optimizations**:
- Only active slides are loaded
- Images use CSS background (efficient)
- JavaScript is minimal and optimized
- Smooth 60fps transitions

**Best Practices**:
- Add 3-5 slides for variety
- Use compressed images
- Enable browser caching
- Consider lazy loading for large images

## Styling Customization

The slider overlay and colors can be customized in `/static/css/styles.css`:

```css
/* Hero overlay - adjust transparency and colors */
.hero-overlay {
  background: linear-gradient(
    to right,
    rgba(11, 110, 79, 0.98) 0%,    /* Dark green left */
    rgba(11, 110, 79, 0.85) 50%,   /* Medium green center */
    rgba(6, 77, 57, 0.7) 100%      /* Light green right */
  );
}

/* Slider dot colors */
.slider-dot {
  background: rgba(255, 255, 255, 0.4); /* Inactive dot */
}

.slider-dot.active {
  background: var(--accent-gold);       /* Active dot - gold */
  border-color: white;
}
```

## Troubleshooting

### Slides Not Showing

**Problem**: Hero shows placeholder instead of your slides

**Solutions**:
1. Check that slides are marked as "Is Active" in admin
2. Verify image URLs are correct and accessible
3. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
4. Check browser console for errors (F12)

### Images Not Loading

**Problem**: Broken images or blank backgrounds

**Solutions**:
1. Verify the image URL loads in a new browser tab
2. Check if the image host allows external linking
3. Use direct image URLs (not webpage URLs)
4. Ensure URLs use HTTPS (not HTTP)

### Slider Not Auto-Rotating

**Problem**: Slides don't change automatically

**Solutions**:
1. Check if you have more than one active slide
2. Clear browser cache and reload
3. Check browser console for JavaScript errors
4. Ensure `/static/js/hero-slider.js` is loaded

### Dots Not Appearing

**Problem**: Navigation dots missing

**Solutions**:
1. Ensure you have 2 or more active slides
2. Dots only show when multiple slides exist
3. Check CSS is properly loaded

### Slow Loading

**Problem**: Hero section loads slowly

**Solutions**:
1. Compress images (use TinyPNG or similar)
2. Reduce image resolution if too high
3. Use WebP format for better compression
4. Enable browser caching
5. Consider using a CDN for images

## Accessibility

The slider includes:
- Keyboard navigation support
- Smooth transitions (no flashing)
- Pause on hover for readability
- Alternative text via slide titles

## Browser Support

The slider works on:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)
- ✅ Internet Explorer 11+ (with fallbacks)

## Example Setup

Here's a recommended setup for a gym:

**Slide 1**: "Modern Gym Equipment" (Order: 0)
- Image: Wide shot of gym floor with equipment
- Shows variety of available equipment

**Slide 2**: "Personal Training" (Order: 1)
- Image: Trainer working with client
- Highlights personal attention

**Slide 3**: "Group Fitness Classes" (Order: 2)
- Image: Energetic group class in action
- Shows community atmosphere

**Slide 4**: "State-of-Art Facilities" (Order: 3)
- Image: Clean, modern facility
- Demonstrates quality standards

**Slide 5**: "Results-Focused" (Order: 4)
- Image: Member achieving fitness goals
- Inspires potential clients

## Updates and Maintenance

### Adding New Slides
- Periodically refresh images to keep content fresh
- Seasonal images (New Year, Summer Body, etc.)
- Feature special events or new equipment

### Removing Old Slides
- Deactivate outdated slides instead of deleting
- Keep for historical reference
- Can reactivate later if needed

### Testing
- Always preview new slides before activating
- Test on multiple devices
- Check load times with new images

## Support

For issues or questions:
1. Check this guide first
2. Review Django logs for errors
3. Inspect browser console (F12)
4. Verify image URLs are accessible

---

## Quick Start Checklist

- [ ] Access admin panel at `/admin/`
- [ ] Navigate to CMS > Hero Slides
- [ ] Add first slide with title and image URL
- [ ] Set Order to 0
- [ ] Check "Is Active"
- [ ] Save slide
- [ ] Add 2-4 more slides
- [ ] Test on home page
- [ ] Verify auto-rotation works
- [ ] Check mobile responsiveness

**Congratulations!** Your hero slider is now ready and fully functional!
