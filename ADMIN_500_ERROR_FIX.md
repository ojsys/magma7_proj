# Admin 500 Error Fix Guide

## Problem Summary

Two admin pages were throwing 500 Server Errors on production:

1. **Memberships Plans Admin** (`/admin/memberships/plan/`)
   - Error: `KeyError: '0'`
   - Cause: MySQL storing boolean values as string '0' instead of integer 0

2. **Error Log Admin** (`/admin/cms/errorlog/`)
   - Error: `ValueError: Database returned an invalid datetime value. Are time zone definitions for your database installed?`
   - Cause: MySQL timezone tables not loaded + `date_hierarchy` feature trying to use timezone functions

---

## Root Causes

### Issue 1: BooleanField KeyError

**What happened:**
- Django's BooleanField expects Python boolean values (True/False) or integers (1/0)
- MySQL was storing the string '0' instead of integer 0
- When Django tried to display the boolean field, it looked up '0' in a dictionary that only had True/False/1/0 keys
- Result: `KeyError: '0'`

**Affected fields:**
- `memberships_plan.is_featured`
- `memberships_plan.is_active`
- `cms_errorlog.resolved`

### Issue 2: MySQL Timezone Error

**What happened:**
- Django admin's `date_hierarchy` feature provides drill-down navigation by date (year → month → day)
- This feature requires MySQL to have timezone data loaded (`mysql_tzinfo_to_sql`)
- cPanel shared hosting usually doesn't have timezone tables loaded (requires root access)
- When `date_hierarchy = 'timestamp'` is used, Django queries timezone functions
- Result: `ValueError: Database returned an invalid datetime value`

---

## The Fix

We fixed both issues with three changes:

### 1. Updated `magma7/settings/production.py`

Added timezone configuration to MySQL database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'",  # ADDED
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,
        'TIME_ZONE': 'UTC',  # ADDED - Fallback timezone
    }
}
```

This sets UTC timezone for all MySQL connections.

### 2. Fixed Database Boolean Values

Converted string '0' to integer 0 in the database using SQL updates:

```sql
-- Fix memberships_plan
UPDATE memberships_plan SET is_featured = 0 WHERE is_featured = '0' OR is_featured = '' OR is_featured IS NULL;
UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = '1';
UPDATE memberships_plan SET is_active = 0 WHERE is_active = '0' OR is_active = '' OR is_active IS NULL;
UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1';

-- Fix cms_errorlog
UPDATE cms_errorlog SET resolved = 0 WHERE resolved = '0' OR resolved = '' OR resolved IS NULL;
UPDATE cms_errorlog SET resolved = 1 WHERE resolved = '1';
```

### 3. Updated `cms/admin.py`

Disabled `date_hierarchy` feature in ErrorLogAdmin:

```python
@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = (...)
    list_filter = (...)
    search_fields = (...)
    readonly_fields = (...)
    ordering = ('-timestamp',)  # ADDED - Show newest errors first
    # date_hierarchy = 'timestamp'  # DISABLED - Requires MySQL timezone tables
```

Now errors are sorted by newest first, and you can still filter by date using `list_filter`.

---

## Deployment Instructions

### Step 1: Upload Files to cPanel

Use **cPanel File Manager** to upload these two files:

1. **Upload `magma7/settings/production.py`**
   - Navigate to: `/home/magmafit/magma7_proj/magma7/settings/`
   - Upload: `production.py` (overwrite existing)

2. **Upload `cms/admin.py`**
   - Navigate to: `/home/magmafit/magma7_proj/cms/`
   - Upload: `admin.py` (overwrite existing)

### Step 2: Run Deployment Script

1. Open **cPanel Terminal**

2. Navigate to project directory:
   ```bash
   cd /home/magmafit/magma7_proj
   ```

3. Run the deployment script:
   ```bash
   bash deploy_admin_fixes.sh
   ```

4. Answer "yes" when prompted about uploading files

### Step 3: Verify the Fix

Visit these admin pages and verify they work:

1. **Memberships Plans:**
   ```
   https://www.magma7fitness.com/admin/memberships/plan/
   ```
   - Should show list of plans with is_featured and is_active checkboxes
   - No KeyError

2. **Error Logs:**
   ```
   https://www.magma7fitness.com/admin/cms/errorlog/
   ```
   - Should show list of errors sorted by newest first
   - Filter by date using sidebar
   - No timezone error

---

## What the Deployment Script Does

The `deploy_admin_fixes.sh` script performs these actions:

1. **Activates virtual environment** and sets production settings
2. **Fixes boolean fields** in database (string '0' → integer 0)
3. **Verifies settings** - checks that timezone config was applied
4. **Tests admin pages** - loads Plans and ErrorLog to confirm they work
5. **Restarts application** - touches `passenger_wsgi.py`

### Sample Output

```
==========================================
Deploying Admin Error Fixes
==========================================

Step 1: Fixing BooleanField values in database...
---------------------------------------
Fixing memberships_plan table...
  Fixed is_featured (set to 0): 3 rows
  Fixed is_featured (set to 1): 1 rows
  Fixed is_active (set to 0): 0 rows
  Fixed is_active (set to 1): 4 rows

Fixing cms_errorlog table...
  Fixed resolved (set to 0): 12 rows
  Fixed resolved (set to 1): 0 rows

✓ Boolean fields fixed!

Step 2: Verifying settings update...
---------------------------------------
Database timezone configuration:
  init_command: SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'
  charset: utf8mb4
  TIME_ZONE: UTC

✓ Settings verified

Step 3: Testing admin pages...
---------------------------------------

✓ Memberships Plans: 4 plans found
  - Monthly: featured=False, active=True
  - Quarterly: featured=True, active=True
  - Semi-Annual: featured=False, active=True
  - Annual: featured=False, active=True

✓ Error Logs: 12 total errors
  Showing latest 5 errors:
  - [ERROR] invalid literal for int() with base 10: '0'
  - [ERROR] Database returned an invalid datetime value
  - [WARNING] Missing logo file
  - [INFO] User login attempt
  - [DEBUG] Database query

Step 4: Restarting application...
---------------------------------------
✓ Application restarted (touched passenger_wsgi.py)

==========================================
✓ Deployment Complete!
==========================================
```

---

## Technical Details

### Why Did This Happen?

1. **Boolean Storage:**
   - When migrating from SQLite to MySQL, boolean values may have been stored as strings
   - Or when creating records via Django shell/forms, validation might have accepted strings
   - MySQL's TINYINT(1) type can store both strings and integers

2. **Timezone Tables:**
   - MySQL doesn't include timezone data by default
   - Requires running `mysql_tzinfo_to_sql` (needs root access)
   - cPanel shared hosting typically doesn't have this loaded
   - Django's `date_hierarchy` feature tries to use timezone-aware queries

### Alternative Solutions Considered

#### For Boolean Issue:
- ❌ Change model field type - Would require migration, doesn't fix existing data
- ❌ Custom form validation - Doesn't fix existing data
- ✅ **Database update** - Direct fix, handles all existing data

#### For Timezone Issue:
- ❌ Load MySQL timezone tables - Requires root access (not available on cPanel)
- ❌ Use SQLite for admin - Complicates deployment
- ✅ **Disable date_hierarchy** - Simple, no functionality loss (can still filter by date)

### Prevention

To prevent this in the future:

1. **Always use proper boolean values:**
   ```python
   plan.is_featured = True  # ✓ Correct
   plan.is_featured = 1     # ✓ Also correct
   plan.is_featured = '1'   # ✗ Wrong - will cause issues
   ```

2. **Avoid date_hierarchy on cPanel:**
   - Use `list_filter` instead for date filtering
   - Or use `ordering = ('-date_field',)` for chronological sorting

3. **Test admin pages after database migrations:**
   - SQLite → MySQL migrations can cause type mismatches
   - Always test all admin pages on production

---

## Error Log Reference

### Original Errors from cPanel

#### Error 1: BooleanField KeyError
```
File "/home/magmafit/virtualenv/magma7_proj/3.12/lib/python3.12/site-packages/django/contrib/admin/templatetags/admin_list.py", line 544, in items_for_result
    f = empty_value_display if result_repr == EMPTY_CHANGELIST_VALUE else conditional_escape(result_repr)
File "/home/magmafit/virtualenv/magma7_proj/3.12/lib/python3.12/site-packages/django/utils/html.py", line 55, in conditional_escape
    return mark_safe(str(s))
File "/home/magmafit/virtualenv/magma7_proj/3.12/lib/python3.12/site-packages/django/db/models/fields/__init__.py", line 1012, in __str__
    return self.label % {'value': _('Unknown')}
KeyError: '0'
```

**Translation:** Django tried to format a boolean field's display value, but found '0' (string) when it expected True/False/0/1.

#### Error 2: Timezone ValueError
```
File "/home/magmafit/virtualenv/magma7_proj/3.12/lib/python3.12/site-packages/django/contrib/admin/templatetags/admin_list.py", line 470, in date_hierarchy
    year_lookup = queryset.dates(field_name, 'year')
File "/home/magmafit/virtualenv/magma7_proj/3.12/lib/python3.12/site-packages/django/db/backends/mysql/operations.py", line 282, in convert_datetimefield_value
    raise ValueError("Database returned an invalid datetime value. Are time zone definitions for your database installed?")
ValueError: Database returned an invalid datetime value. Are time zone definitions for your database installed?
```

**Translation:** Django tried to extract year from timestamps using timezone functions, but MySQL timezone tables weren't loaded.

---

## Rollback Plan

If something goes wrong, you can rollback:

### Option 1: Restore from Backup
If you have backups of `production.py` and `admin.py`, restore them and restart.

### Option 2: Manual Revert

1. **Revert `production.py`:**
   Remove the timezone configuration from `OPTIONS`:
   ```python
   'OPTIONS': {
       'charset': 'utf8mb4',
   },
   ```

2. **Revert `admin.py`:**
   Re-enable date_hierarchy:
   ```python
   date_hierarchy = 'timestamp'
   # ordering = ('-timestamp',)
   ```

3. **Restart:**
   ```bash
   touch passenger_wsgi.py
   ```

---

## Next Steps After Fix

1. **Set Featured Membership Plan:**
   - See `SET_FEATURED_PLAN.md`
   - Recommended: Feature the Quarterly (3-month) plan
   - Only ONE plan should be featured at a time

2. **Monitor Error Logs:**
   - Visit: `https://www.magma7fitness.com/admin/cms/errorlog/`
   - Check for new errors
   - Mark resolved errors

3. **Test All Admin Pages:**
   - Go through each admin section
   - Verify everything loads correctly
   - Report any remaining issues

---

## Support

If errors persist after deployment:

1. **Check cPanel Error Logs:**
   - cPanel → Errors
   - Look for new Python exceptions

2. **Check Django Error Logs:**
   - Admin → CMS → Error logs
   - Filter by severity: ERROR or CRITICAL

3. **Verify Files Were Uploaded:**
   - Check file timestamps in File Manager
   - Ensure `production.py` and `admin.py` were updated

4. **Check Settings Module:**
   ```bash
   cd /home/magmafit/magma7_proj
   source ~/virtualenv/magma7_proj/3.12/bin/activate
   python manage.py shell
   ```
   ```python
   from django.conf import settings
   print(settings.DATABASES['default']['OPTIONS'])
   # Should show: {'init_command': "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'", 'charset': 'utf8mb4'}
   ```

---

## Summary

**Problem:** Admin pages throwing 500 errors due to boolean string values and missing MySQL timezone tables

**Solution:**
- ✓ Fixed boolean fields in database (string → integer)
- ✓ Added timezone configuration to production settings
- ✓ Disabled date_hierarchy feature (replaced with ordering)

**Files Changed:**
- `magma7/settings/production.py` (lines 37-42)
- `cms/admin.py` (lines 354-355)

**Deployment:**
1. Upload files via cPanel File Manager
2. Run `bash deploy_admin_fixes.sh`
3. Verify admin pages work

**Status:** Ready to deploy ✓

---

**Last Updated:** 2025-10-20
