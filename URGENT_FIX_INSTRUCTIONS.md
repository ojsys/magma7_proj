# URGENT: Fix Boolean Fields Error on Production

## The Error

Your admin page is showing `KeyError: '0'` because MySQL is storing boolean values as strings instead of integers.

---

## Quick Fix (Choose ONE method)

### Method 1: Using Django Management Command (RECOMMENDED)

This is the safest and cleanest method.

#### Step 1: Upload the fix
1. Upload `memberships/management/` folder to cPanel:
   - Navigate to: `/home/magmafit/magma7_proj/memberships/`
   - Upload the entire `management` folder (contains `__init__.py`, `commands/` subfolder)

#### Step 2: Run the command
Open cPanel Terminal and run:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

python manage.py fix_boolean_fields
```

#### Step 3: Restart application
```bash
touch passenger_wsgi.py
```

#### Step 4: Test
Visit: https://www.magma7fitness.com/admin/memberships/plan/

Should work now! ✓

---

### Method 2: Using Bash Script (ALTERNATIVE)

If you prefer using a bash script instead.

#### Step 1: Upload script
Upload `fix_boolean_fields_now.sh` to `/home/magmafit/magma7_proj/`

#### Step 2: Run script
Open cPanel Terminal and run:

```bash
cd /home/magmafit/magma7_proj
bash fix_boolean_fields_now.sh
```

The script will:
- Show current boolean values
- Fix them to proper integers (0 or 1)
- Verify the fix
- Restart the application

#### Step 3: Test
Visit: https://www.magma7fitness.com/admin/memberships/plan/

---

## What This Fix Does

The fix converts:
- String `'0'` → Integer `0` (False)
- String `'1'` → Integer `1` (True)
- Empty string `''` → Integer `0` (False)
- NULL → Integer `0` (False)

### Fields Fixed:
- `memberships_plan.is_featured`
- `memberships_plan.is_active`

---

## Expected Output

### Good Output:
```
Fixed data (4 plans):
  ID: 1, Name: Monthly, is_featured: 0 (int), is_active: 1 (int)
  ID: 2, Name: Quarterly, is_featured: 1 (int), is_active: 1 (int)
  ID: 3, Name: Semi-Annual, is_featured: 0 (int), is_active: 1 (int)
  ID: 4, Name: Annual, is_featured: 0 (int), is_active: 1 (int)
```

Notice the `(int)` - this means the value is a proper integer, not a string.

### Bad Output (needs fixing):
```
Current data (4 plans):
  ID: 1, Name: Monthly, is_featured: '0' (str), is_active: '1' (str)
```

Notice the quotes around values - this means they're strings, which causes the error.

---

## Why This Happened

When you created plans in the database, the boolean fields were stored as strings (`'0'` and `'1'`) instead of integers (0 and 1). This happens when:

1. Data is imported from another database
2. Values are inserted via raw SQL
3. Database migration issues

Django's admin expects boolean fields to be proper integers, so when it sees `'0'` (string), it crashes with `KeyError: '0'`.

---

## Prevention

After running the fix, always use Django ORM to create/update plans:

**✓ Correct way:**
```python
from memberships.models import Plan

plan = Plan.objects.create(
    name="Monthly",
    price=25000,
    duration_days=30,
    is_featured=False,  # or True, not '0' or '1'
    is_active=True
)
```

**✗ Wrong way:**
```python
# Don't do this:
plan.is_featured = '0'  # Wrong - this is a string!
plan.save()
```

---

## Troubleshooting

### If the fix doesn't work:

1. **Check you're using production settings:**
   ```bash
   echo $DJANGO_SETTINGS_MODULE
   # Should output: magma7.settings.production
   ```

2. **Check database connection:**
   ```bash
   python manage.py dbshell
   ```
   Then run:
   ```sql
   SELECT id, name, is_featured, is_active FROM memberships_plan;
   ```

   If you see quotes around 0 and 1, the fix didn't apply.

3. **Manually fix in MySQL:**
   ```sql
   UPDATE memberships_plan SET is_featured = 0 WHERE is_featured != 1;
   UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = 1;
   UPDATE memberships_plan SET is_active = 0 WHERE is_active != 1;
   UPDATE memberships_plan SET is_active = 1 WHERE is_active = 1;
   ```

4. **Check for other boolean fields:**
   If you still get errors, check `cms_errorlog.resolved` field:
   ```bash
   python manage.py shell
   ```
   ```python
   from cms.models import ErrorLog
   ErrorLog.objects.all().update(resolved=False)  # Reset all to False
   ```

---

## After Fix is Complete

Once the admin page loads successfully:

1. **Set featured plan:**
   - Go to admin → Memberships → Plans
   - Edit the Quarterly plan
   - Check "Is featured"
   - Save

2. **Deploy other fixes:**
   - Follow `ADMIN_FIX_CHECKLIST.md` to deploy:
     - Updated `production.py` (timezone fix)
     - Updated `admin.py` (date_hierarchy fix)

---

## Files Included in This Fix

1. **`memberships/management/commands/fix_boolean_fields.py`**
   - Django management command
   - Safe, clean, recommended method

2. **`fix_boolean_fields_now.sh`**
   - Bash script alternative
   - Quick fix for emergencies

Choose whichever method you're more comfortable with!

---

## Summary

**Problem:** Boolean fields stored as strings → `KeyError: '0'`

**Solution:** Convert string values to integers

**Time to fix:** 2-3 minutes

**Risk:** Low - only updates existing values to proper type

**Impact:** Admin pages will work immediately

---

**Questions?** Check `ADMIN_500_ERROR_FIX.md` for full technical details.

**Status:** Ready to deploy - choose Method 1 or Method 2 above ✓
