# How to Set Featured Plan (Most Popular Badge)

## Current Setup

The "Most Popular" badge will **only** show on plans where `is_featured = True` in the database. By default, all plans have `is_featured = False`, so no badge will show unless you manually set it.

---

## How to Mark a Plan as Featured

### Option 1: Django Admin (Recommended)

1. **Go to Django Admin**:
   - Local: `http://localhost:8000/admin/`
   - Production: `https://www.magma7fitness.com/admin/`

2. **Navigate to Plans**:
   - Click **"Memberships"** section
   - Click **"Plans"**

3. **Edit the Plan You Want to Feature**:
   - Click on the plan you want to mark as "Most Popular" (e.g., Quarterly)
   - Check the **"Is featured"** checkbox
   - Click **"Save"**

4. **Uncheck Other Plans** (if any were featured):
   - Only ONE plan should be featured at a time
   - Go through other plans and uncheck "Is featured" if checked

5. **Refresh the Plans Page**:
   - Visit `/memberships/plans/`
   - Only the featured plan will show the gold "Most Popular" badge

---

## Recommended: Feature the Quarterly Plan

Based on common gym membership patterns, here's what you should feature:

### Best Practice:
**Feature the plan that offers the best value** (usually 3-6 months)

**Why?**
- Encourages longer commitment
- Better retention rates
- Shows customers the "sweet spot" pricing
- Industry standard for gym memberships

### Example Setup:

| Plan | Duration | Featured? | Why |
|------|----------|-----------|-----|
| Monthly | 1 month | ❌ No | Highest per-month cost |
| **Quarterly** | **3 months** | **✅ Yes** | **Best value, recommended** |
| Semi-Annual | 6 months | ❌ No | Good value but longer commitment |
| Annual | 12 months | ❌ No | Best price but too long for new customers |

---

## Future: Auto-Feature Most Subscribed Plan

If you want to automatically feature the plan with the most active subscriptions, you can add this logic later. For now, manually set the featured plan in admin.

### To implement auto-featuring (optional):

1. Count active subscriptions per plan
2. Mark the plan with most subscriptions as featured
3. Run this as a periodic task (weekly/monthly)

**For now, just manually set it in admin** - it's simpler and you have full control.

---

## Checking Current Featured Status

### Via Django Admin:
1. Go to Plans list
2. Look at the "Is featured" column
3. Should see ✓ for one plan, blank for others

### Via Django Shell:
```bash
python manage.py shell
```

```python
from memberships.models import Plan

# Show all plans and their featured status
for plan in Plan.objects.all():
    print(f"{plan.name}: Featured = {plan.is_featured}")

# Set Quarterly as featured
quarterly = Plan.objects.get(name__icontains="Quarterly")
quarterly.is_featured = True
quarterly.save()

# Unfeature all other plans
Plan.objects.exclude(id=quarterly.id).update(is_featured=False)

print("\nQuarterly plan is now featured!")
```

---

## Visual Indicators

When a plan is featured:
- **Gold border** around the entire card
- **"Most Popular" badge** in top-right corner (gold background)
- **Slightly larger** card size (scaled 1.05x)
- **Stands out** from other plans

When NOT featured:
- Regular white card with shadow
- No badge
- Normal size
- Hover effects still work

---

## Quick Setup Command

Run this on your server to feature the Quarterly plan:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

python manage.py shell << 'PYEOF'
from memberships.models import Plan

# Find Quarterly plan (adjust name if different)
try:
    quarterly = Plan.objects.get(name__icontains="Quarterly")
    quarterly.is_featured = True
    quarterly.save()
    print(f"✓ {quarterly.name} is now featured!")
except Plan.DoesNotExist:
    print("✗ Quarterly plan not found. Available plans:")
    for p in Plan.objects.all():
        print(f"  - {p.name}")

# Unfeature all others
Plan.objects.filter(is_featured=True).exclude(name__icontains="Quarterly").update(is_featured=False)
print("✓ All other plans unfeatured")
PYEOF
```

---

## Testing

After setting featured plan:

1. **Visit Plans Page**:
   ```
   https://www.magma7fitness.com/memberships/plans/
   ```

2. **Check for Badge**:
   - Should see "MOST POPULAR" badge on one plan only
   - That plan should have gold border
   - Other plans should be normal

3. **Test Responsiveness**:
   - Check on mobile - badge should still be visible
   - Featured card should look good on all screen sizes

---

## Summary

✅ **The badge only shows on plans with `is_featured=True`**

✅ **By default, NO plans are featured** (all start with `is_featured=False`)

✅ **You need to manually set ONE plan as featured** in Django admin

✅ **Recommended: Feature your 3-month (Quarterly) plan** for best results

✅ **Only ONE plan should be featured at a time**

---

## Next Steps

1. Go to Django admin
2. Click Memberships → Plans
3. Edit your Quarterly plan (or whichever you want featured)
4. Check "Is featured"
5. Save
6. Refresh the plans page - badge should appear!

Done! 🎉
