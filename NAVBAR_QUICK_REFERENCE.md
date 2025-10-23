# Navigation Quick Reference

## Desktop Navigation (>1024px)

```
┌─────────────────────────────────────────────────────────────┐
│ [Logo]        About Facilities Team ... │ 🔔 Dashboard Logout │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Logo: Far left, scales on hover
- Menu: Center-right, underline on hover
- Auth: Far right with divider
- Sticky: Stays at top when scrolling

---

## Mobile Navigation (≤1024px)

```
┌─────────────────────────────────┐
│ [Logo]                     [☰]  │  ← Navbar (70-90px)
└─────────────────────────────────┘
         ↓ (tap hamburger)
┌─────────────────────────────────┐
│ About                           │
│ Facilities                      │
│ Team                            │
│ Testimonials                    │
│ Membership Plans                │
│ ────────────────────            │
│ Login                           │
│ [Join Now]                      │
└─────────────────────────────────┘
```

**Features:**
- Hamburger: Animates to X
- Menu: Full-width dropdown
- Backdrop: Blur + fade
- Auto-close: On click or outside tap

---

## Key Classes

### HTML Structure
```html
<nav class="navbar-main">
  <div class="navbar-container">
    <a class="navbar-logo">...</a>
    <div class="navbar-menu">...</div>
    <button class="mobile-menu-toggle">...</button>
  </div>
  <div class="mobile-menu">...</div>
</nav>
```

### Important CSS

```css
/* Desktop */
.navbar-main         /* Main container */
.navbar-container    /* Content wrapper */
.navbar-menu         /* Desktop menu */
.nav-item           /* Menu links */

/* Mobile */
.mobile-menu-toggle  /* Hamburger button */
.mobile-menu        /* Overlay menu */
.mobile-nav-item    /* Mobile links */
```

---

## Responsive Breakpoints

| Screen Size | Navbar Height | Logo Height | Behavior |
|-------------|---------------|-------------|----------|
| >1024px     | 90px          | 70px        | Horizontal menu |
| 769-1024px  | 90px          | 70px        | Hamburger menu |
| 481-768px   | 80px          | 60px        | Hamburger menu |
| ≤480px      | 70px          | 50px        | Hamburger menu |

---

## JavaScript Functions

```javascript
// Open/close mobile menu
mobileMenuToggle.click()

// Auto-closes on:
- Menu item click
- Outside click
- Window resize (>1024px)
- Escape key (could add)
```

---

## Common Customizations

### Change Colors
```css
:root {
  --primary-green: #0b6e4f;  /* Main color */
  --accent-gold: #d4af37;    /* Accent */
}
```

### Change Height
```css
.navbar-container {
  height: 90px; /* Adjust here */
}
```

### Change Breakpoint
```css
@media screen and (max-width: 1024px) { /* Change this */
  .navbar-menu { display: none; }
  .mobile-menu-toggle { display: flex; }
}
```

### Disable Sticky
```css
.navbar-main {
  position: relative; /* Instead of sticky */
}
```

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| HTML | `/templates/base.html` | Navbar structure |
| CSS | `/static/css/styles.css` | Navbar styles (lines 85-469) |
| JS | Inline in `base.html` | Mobile menu toggle |

---

## Quick Deploy

```bash
# Upload files to cPanel
templates/base.html → /home/magmafit/magma7_proj/templates/
static/css/styles.css → /home/magmafit/magma7_proj/static/css/

# Run in terminal
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py collectstatic --noinput
touch passenger_wsgi.py
```

---

## Testing URLs

**Local:**
- http://localhost:8000/

**Production:**
- https://www.magma7fitness.com/

**Test Pages:**
- / (Home)
- /about/ (About)
- /facilities/ (Facilities)
- /memberships/plans/ (Plans)

---

## Browser DevTools Testing

**Desktop:**
1. F12 → Inspect
2. Resize browser window
3. Check: 1920px, 1440px, 1024px

**Mobile:**
1. F12 → Toggle Device Toolbar
2. Select: iPhone 12, iPad, Samsung Galaxy
3. Test: Portrait & Landscape

**Network:**
1. Throttle to 3G
2. Test menu responsiveness
3. Check animation smoothness

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Menu overlaps logo | Check `justify-content: space-between` |
| Hamburger not clicking | Check JavaScript console |
| No animations | Clear cache, reload |
| Menu stays open | Check event listeners |
| Wrong height on mobile | Check media queries |

---

## Features Checklist

Desktop:
- [x] Logo left aligned
- [x] Menu right aligned
- [x] Proper spacing
- [x] Hover effects
- [x] Notification badge
- [x] Sticky behavior

Mobile:
- [x] Hamburger icon
- [x] Animated transform
- [x] Full-screen menu
- [x] Backdrop blur
- [x] Touch-friendly
- [x] Auto-close

Both:
- [x] Responsive logo
- [x] Smooth transitions
- [x] Accessible
- [x] Fast performance

---

**Status:** ✓ Production Ready
**Version:** 2.0 (Complete Rebuild)
**Last Updated:** 2025-10-22
