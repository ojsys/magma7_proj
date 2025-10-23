# Navigation Visual Guide

## Desktop Navigation

### Layout Structure

```
┌──────────────────────────────────────────────────────────────────────┐
│  Navbar Container (max-width: 1400px, centered)                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                                                                │  │
│  │  [Logo]                                          Menu Section  │  │
│  │   70px                                                         │  │
│  │   height       About  Facilities  Team  ...  │ 🔔 Login Join  │  │
│  │                                               │                │  │
│  │                                          Auth Section ────────>│  │
│  │                                        (separated by border)   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  Height: 90px                                                         │
└──────────────────────────────────────────────────────────────────────┘
        ↑                                                          ↑
   Flex start                                                 Flex end
```

### Spacing Breakdown

```
┌─────┬──────────────────────────────┬───────┬──────────┐
│Logo │      Flexible Space          │  Menu │   Auth   │
│70px │      (auto-expands)          │ Items │ Section  │
└─────┴──────────────────────────────┴───────┴──────────┘
  ↑                                      ↑         ↑
  Far left                          Right side   Far right
```

### Hover States

**Before Hover:**
```
About

```

**On Hover:**
```
About    ← Background: rgba(11, 110, 79, 0.05)
──────   ← Underline: 2px, animates from 0 to 100% width
```

---

## Mobile Navigation

### Closed State

```
┌─────────────────────────────────────┐
│                                     │
│  [Logo]                       [☰]  │  ← Hamburger (3 lines)
│   60px                         32px │
│                                     │
└─────────────────────────────────────┘
Height: 70-90px (responsive)
```

### Open State - Hamburger Animation

```
Step 1: Closed        Step 2: Opening       Step 3: Open
   ═══                    ╱                     ╲
   ═══                   ═══         →           ╳
   ═══                    ╲                     ╱

(3 parallel lines)  (rotating)          (X shape)
```

### Open State - Menu

```
┌─────────────────────────────────────┐
│  [Logo]                       [✕]  │  ← Navbar stays visible
└─────────────────────────────────────┘
        ↓ Slides down with blur backdrop
┌─────────────────────────────────────┐
│ ╔═════════════════════════════════╗ │
│ ║  About                          ║ │ ← Menu slides in
│ ║                                 ║ │
│ ║  Facilities                     ║ │
│ ║                                 ║ │
│ ║  Team                           ║ │
│ ║                                 ║ │
│ ║  Testimonials                   ║ │
│ ║                                 ║ │
│ ║  Membership Plans               ║ │
│ ║                                 ║ │
│ ║  ─────────────────────          ║ │ ← Divider
│ ║                                 ║ │
│ ║  Login                          ║ │
│ ║                                 ║ │
│ ║  [Join Now]                     ║ │ ← CTA button
│ ╚═════════════════════════════════╝ │
│                                     │
│       Backdrop (blur + fade)        │
│                                     │
└─────────────────────────────────────┘
```

---

## Responsive Breakpoints

### Desktop (>1024px)

```
Screen: ████████████████████████████████████
        [Logo]              Menu Items ... Auth
Navbar: ════════════════════════════════════
Height: 90px
Logo:   70px
```

### Tablet Landscape (769-1024px)

```
Screen: ████████████████████████
        [Logo]            [☰]
Navbar: ════════════════════════
Height: 90px
Logo:   70px
Menu:   Hamburger
```

### Tablet Portrait (481-768px)

```
Screen: ████████████████
        [Logo]      [☰]
Navbar: ════════════════
Height: 80px
Logo:   60px
Menu:   Hamburger
```

### Mobile (≤480px)

```
Screen: ██████████
        [Logo] [☰]
Navbar: ══════════
Height: 70px
Logo:   50px
Menu:   Hamburger
```

---

## Color States

### Navigation Links

**Default State:**
```
Text: #4a5568 (var(--text-secondary))
Background: transparent
```

**Hover State:**
```
Text: #0b6e4f (var(--primary-green))
Background: rgba(11, 110, 79, 0.05)
Underline: #0b6e4f, 2px
```

**Active/Current:**
```
Text: #0b6e4f (var(--primary-green))
Font-weight: 600
```

### Buttons

**Primary Button (Join):**
```
Default:
  Background: #0b6e4f (green)
  Text: #ffffff (white)
  Border: 2px solid #0b6e4f

Hover:
  Background: #064d39 (darker green)
  Transform: translateY(-2px)
  Shadow: 0 4px 12px rgba(11, 110, 79, 0.4)
```

**Outline Button (Logout):**
```
Default:
  Background: transparent
  Text: #0b6e4f (green)
  Border: 2px solid #0b6e4f

Hover:
  Background: #0b6e4f (green)
  Text: #ffffff (white)
  Transform: translateY(-2px)
```

### Notification Badge

```
Position: Top-right of bell icon
  ┌──────┐
  │  🔔  │ ← Bell icon
  │    ⓷ │ ← Badge (absolute positioned)
  └──────┘

Badge Styles:
  Background: #dc2626 (red)
  Text: #ffffff (white)
  Size: 18px diameter
  Position: top: 4px, right: 4px
```

---

## Animation Timeline

### Page Load
```
Frame 1:  Navbar renders
Frame 2:  Fade in (if added)
Duration: Instant (or 200ms fade)
```

### Desktop Link Hover
```
Frame 1:  Default state
Frame 2:  Background fades in (150ms)
Frame 3:  Underline scales from 0 to 1 (300ms)
Duration: 300ms total
Easing:   ease
```

### Mobile Menu Open
```
Frame 1:  Hamburger default (3 lines)
Frame 2:  Top/bottom lines rotate (200ms)
Frame 3:  Middle line fades out (200ms)
Frame 4:  Forms X shape

Frame 5:  Backdrop fades in (300ms)
Frame 6:  Menu slides down (300ms)
Duration: 300ms
Easing:   ease
```

### Mobile Menu Close
```
Frame 1:  X shape
Frame 2:  Reverse rotation (200ms)
Frame 3:  Middle line fades in (200ms)
Frame 4:  Back to 3 lines

Frame 5:  Menu slides up (300ms)
Frame 6:  Backdrop fades out (300ms)
Duration: 300ms
Easing:   ease
```

---

## Touch Targets (Mobile)

### Minimum Sizes
```
Element              Width    Height   Accessible?
─────────────────────────────────────────────────
Mobile nav item      100%     48px+    ✅ Yes
Hamburger button     44px     44px     ✅ Yes
Logo                 120px+   50px     ✅ Yes
Mobile CTA button    100%     48px     ✅ Yes
```

**Recommended:** 44x44px minimum (Apple HIG)
**Implemented:** 48px+ for comfort

---

## Z-Index Hierarchy

```
Layer                    Z-Index    Purpose
──────────────────────────────────────────────
Mobile toggle button     1001       Always clickable
Navbar main             1000       Above content
Mobile menu backdrop    999        Overlay content
Mobile menu content     999        Same as backdrop
Page content            1          Normal flow
Footer                  1          Normal flow
```

---

## Accessibility Features

### Keyboard Navigation

```
Tab Order:
1. Logo (link)
2. About (link)
3. Facilities (link)
4. Team (link)
5. Testimonials (link)
6. Membership (link)
7. Notification (button)
8. Dashboard/Login (link)
9. Logout/Join (button)
```

### Screen Reader

```
<nav class="navbar-main">           ← Landmark
  <a href="/">...</a>                ← Link
  <button aria-label="Toggle menu"> ← Button with label
    ...
  </button>
</nav>
```

### Focus States

```
Default Focus Ring:
  Outline: 2px solid #0b6e4f
  Outline-offset: 2px

Visible on:
  - Tab navigation
  - Keyboard interaction
```

---

## CSS Class Reference

### Container Classes
```css
.navbar-main         /* Root nav element */
.navbar-container    /* Content wrapper, max-width */
.navbar-logo         /* Logo link */
.navbar-menu         /* Desktop menu wrapper */
.navbar-nav          /* Navigation list */
.navbar-auth         /* Auth section wrapper */
```

### Link Classes
```css
.nav-item           /* Desktop nav links */
.nav-item-highlight /* Featured nav item */
.nav-notification   /* Notification bell */
.notification-badge /* Badge counter */
```

### Button Classes
```css
.btn-primary-nav    /* Primary button (Join) */
.btn-outline-nav    /* Outline button (Logout) */
```

### Mobile Classes
```css
.mobile-menu-toggle  /* Hamburger button */
.hamburger-line      /* Hamburger line (3x) */
.mobile-menu         /* Mobile menu overlay */
.mobile-menu-content /* Menu content area */
.mobile-nav-item     /* Mobile menu link */
.mobile-nav-cta      /* Mobile CTA button */
.mobile-divider      /* Menu section divider */
.mobile-badge        /* Mobile notification badge */
```

---

## Flexbox Layout

### Desktop Container
```css
.navbar-container {
  display: flex;
  justify-content: space-between; ← Key property
  align-items: center;
}

Creates:
[Logo] ←──── auto space ────→ [Menu] [Auth]
```

### Menu Section
```css
.navbar-menu {
  display: flex;
  justify-content: flex-end; ← Pushes to right
  align-items: center;
  flex: 1; ← Takes remaining space
}
```

### Navigation List
```css
.navbar-nav {
  display: flex;
  gap: 0.5rem; ← Space between items
  align-items: center;
}
```

---

## Quick Copy-Paste

### Add New Nav Item (Desktop)
```html
<li><a href="/new-page/" class="nav-item">New Page</a></li>
```

### Add New Nav Item (Mobile)
```html
<a href="/new-page/" class="mobile-nav-item">New Page</a>
```

### Add Dropdown (Future)
```html
<li class="nav-dropdown">
  <a href="#" class="nav-item">Services ▼</a>
  <div class="dropdown-content">
    <a href="/service-1/">Service 1</a>
    <a href="/service-2/">Service 2</a>
  </div>
</li>
```

---

## Testing Checklist

### Visual Testing
- [ ] Logo loads and scales correctly
- [ ] Menu items aligned properly
- [ ] Spacing looks clean
- [ ] Hover effects work smoothly
- [ ] Buttons styled correctly
- [ ] Notification badge visible

### Functional Testing
- [ ] All links navigate correctly
- [ ] Hamburger toggles menu
- [ ] Menu closes on item click
- [ ] Menu closes on outside click
- [ ] Sticky navbar works on scroll
- [ ] Notification badge shows count

### Responsive Testing
- [ ] Test at 1920px (Desktop)
- [ ] Test at 1440px (Laptop)
- [ ] Test at 1024px (Tablet landscape)
- [ ] Test at 768px (Tablet portrait)
- [ ] Test at 375px (iPhone)
- [ ] Test at 360px (Android)

### Accessibility Testing
- [ ] Tab through all links
- [ ] Screen reader announces properly
- [ ] Focus states visible
- [ ] Hamburger has ARIA label
- [ ] Keyboard can close menu

---

**Visual Guide Complete** ✅
**Use with:** `DEPLOY_NEW_NAVBAR.md` and `NAVBAR_QUICK_REFERENCE.md`
