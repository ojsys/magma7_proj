# Deploy Navbar Spacing Fix

## The Issue

On large screens, the logo and navigation menu were overlapping, causing a cluttered appearance.

## The Fix

Updated the navbar CSS to use flexbox with `justify-content: space-between`, ensuring:
- Logo stays on the left
- Menu stays on the right
- Clear space between them
- No overlap regardless of logo size

---

## Quick Deployment Steps

### Step 1: Upload File to cPanel

Use **cPanel File Manager** to upload:

**File:** `static/css/styles.css`
**Location:** `/home/magmafit/magma7_proj/static/css/`

### Step 2: Collect Static Files

Open **cPanel Terminal** and run:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Collect static files
python manage.py collectstatic --noinput

# Restart application
touch passenger_wsgi.py
```

### Step 3: Test

Visit: https://www.magma7fitness.com/

**On large screen:**
- Logo should be on the far left
- Menu items should be on the far right
- Clear space between logo and menu
- No overlap

---

## What Changed

**File:** `static/css/styles.css`

### 1. Nav Wrapper (Line 95-102)
```css
.nav-wrapper {
  padding: 0 40px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;  /* ADDED - Creates space between logo and menu */
  height: 120px;
}
```

### 2. Brand Logo (Line 104-113)
```css
.brand-logo {
  font-weight: 900 !important;
  font-size: 1.8rem !important;
  color: var(--primary-green) !important;
  letter-spacing: -0.5px;
  line-height: 120px;
  position: static !important;    /* ADDED - Prevents absolute positioning */
  left: auto !important;          /* ADDED - Overrides Materialize default */
  transform: none !important;     /* ADDED - Removes centering transform */
}
```

### 3. Right Menu (Line 121-126)
```css
.nav-wrapper ul.right {
  display: flex;              /* ADDED - Flexbox for menu items */
  align-items: center;        /* ADDED - Vertical centering */
  flex-shrink: 0;            /* ADDED - Prevents menu from shrinking */
  margin-left: auto;         /* ADDED - Pushes menu to the right */
}
```

---

## How It Works

**Before:**
- Materialize CSS positioned `.brand-logo` absolutely, centered
- Menu floated right, potentially overlapping logo

**After:**
- Flexbox with `justify-content: space-between`
- Logo stays left (natural position)
- Menu pushed to far right with `margin-left: auto`
- Flex prevents overlap and ensures spacing

---

## Mobile Behavior

This fix only affects **large screens**. On mobile/tablet:
- Hamburger menu is displayed
- Logo remains visible
- Sidenav drawer opens on click
- No overlap issues

The existing mobile CSS (max-width: 992px) remains unchanged.

---

## Deployment Checklist

- [ ] Upload `static/css/styles.css` to `/home/magmafit/magma7_proj/static/css/`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Run `touch passenger_wsgi.py`
- [ ] Test on desktop - verify logo and menu spacing
- [ ] Test on mobile - verify hamburger menu works
- [ ] Check different screen sizes (1920px, 1440px, 1024px)

---

## Expected Result

### Desktop (>992px)
```
[Logo]                                    [About] [Facilities] [Team] [...] [Join]
```

Clear space between logo and navigation items.

### Mobile (<992px)
```
[Logo]                                                            [☰]
```

Hamburger menu icon on the right.

---

## Time to Deploy

**Total time:** ~2 minutes

1. Upload file: 30 seconds
2. Collect static: 30 seconds
3. Restart app: 10 seconds
4. Test: 1 minute

---

## Rollback

If you need to revert:

1. Download the previous version of `styles.css`
2. Upload it back to cPanel
3. Run `collectstatic` and restart

Or restore from your local backup:
```bash
git checkout static/css/styles.css
```

---

## Notes

- This fix works with any logo size
- No changes to HTML/templates needed
- Pure CSS solution using modern flexbox
- Compatible with all modern browsers
- No impact on mobile navigation

---

**Status:** ✓ Fix applied locally
**Ready for:** Production deployment
