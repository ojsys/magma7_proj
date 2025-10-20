# Fix Git Conflicts on cPanel Production

## The Problem

When you ran `git pull`, Git found conflicts between:
- **Local files** (on your Mac) - the cleaned-up migration files
- **Remote files** (on cPanel) - old backup files that shouldn't exist

## Quick Solution

Copy and paste these commands **one at a time** in your cPanel Terminal:

### Step 1: Navigate to project directory
```bash
cd /home/magmafit/magma7_proj
```

### Step 2: Abort the current merge
```bash
git merge --abort
```

### Step 3: Stash any local changes
```bash
git stash
```

### Step 4: Pull fresh changes
```bash
git pull origin main
```

If it still shows conflicts, continue:

### Step 5: Force pull (use with caution)
```bash
git fetch origin
git reset --hard origin/main
```

**⚠️ WARNING:** This will discard ANY local changes on the server. Make sure you don't have important uncommitted changes!

### Step 6: Verify the migration files
```bash
ls -1 cms/migrations/*.py | grep -E "000[1-9]"
```

You should see:
```
cms/migrations/0001_initial.py
cms/migrations/0002_sitesettings_free_guide_description_and_more.py
cms/migrations/0003_sitesettings_cta_description_and_more.py
cms/migrations/0004_aboutgalleryimage_aboutpage_aboutstatistic_corevalue_and_more.py
cms/migrations/0005_facilitiespage_facility_teammember_teampage.py
cms/migrations/0006_heroslide.py
cms/migrations/0007_errorlog.py
cms/migrations/0008_mediaasset_and_more.py
```

### Step 7: Activate virtual environment
```bash
source ~/virtualenv/magma7_proj/3.12/bin/activate
```

### Step 8: Set production settings
```bash
export DJANGO_SETTINGS_MODULE=magma7.settings.production
```

### Step 9: Run migrations
```bash
python manage.py migrate
```

### Step 10: Fix boolean fields (THIS IS THE IMPORTANT ONE!)
```bash
python manage.py fix_boolean_fields
```

### Step 11: Restart application
```bash
touch passenger_wsgi.py
```

### Step 12: Test
Visit: https://www.magma7fitness.com/admin/memberships/plan/

---

## Alternative: Manual Conflict Resolution

If you prefer to manually resolve conflicts:

### Step 1: Accept all incoming changes
```bash
cd /home/magmafit/magma7_proj
git checkout --theirs .
```

### Step 2: Remove backup files
```bash
rm -f cms/migrations/*_BACKUP.py.bak
```

### Step 3: Stage all changes
```bash
git add .
```

### Step 4: Complete the merge
```bash
git commit -m "Resolve migration conflicts - accept incoming changes"
```

### Step 5: Continue from Step 7 above
(Activate venv, set settings, run migrations, fix booleans, restart)

---

## Understanding the Conflicts

### What happened:
1. You cleaned up migrations on your local Mac
2. The cPanel server had old backup files (`.bak` files)
3. Git doesn't know whether to keep the backups or delete them

### The solution:
- **Remove all backup files** - they're not needed
- **Accept the clean migration files** from your Mac
- **Run migrations** to update the database
- **Fix boolean fields** to solve the admin error

---

## Expected Output

### After `git pull` or `git reset`:
```
Already up to date.
```
or
```
HEAD is now at <commit-hash> <commit-message>
```

### After `python manage.py migrate`:
```
Operations to perform:
  Apply all migrations: admin, auth, cms, contenttypes, memberships, notifications, payments, sessions, users
Running migrations:
  No migrations to apply.
```

### After `python manage.py fix_boolean_fields`:
```
==========================================
Fixing Boolean Fields
==========================================

Found 4 plan(s):
  ID: 1, Name: Monthly, is_featured: '0', is_active: '1'
  ...

Fixing is_featured field...
  ✓ Set 3 row(s) to 0
  ✓ Converted 1 string '1' to integer 1

Fixing is_active field...
  ✓ Set 0 row(s) to 0
  ✓ Converted 4 string '1' to integer 1

Fixed data (4 plan(s)):
  ID: 1, Name: Monthly, is_featured: 0 (int), is_active: 1 (int)
  ...

✓ Boolean fields fixed successfully!
```

---

## Troubleshooting

### If `git pull` still fails:
Try the force method (Step 5 above):
```bash
git fetch origin
git reset --hard origin/main
```

### If migrations fail:
Check which migrations are applied:
```bash
python manage.py showmigrations cms
```

Fake apply if needed:
```bash
python manage.py migrate cms --fake
```

### If boolean fix doesn't work:
Run manual SQL:
```bash
python manage.py dbshell
```

Then:
```sql
UPDATE memberships_plan SET is_featured = 0 WHERE is_featured != 1;
UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = 1;
UPDATE memberships_plan SET is_active = 0 WHERE is_active != 1;
UPDATE memberships_plan SET is_active = 1 WHERE is_active = 1;
exit;
```

---

## Summary

**Quick Fix:**
```bash
cd /home/magmafit/magma7_proj
git merge --abort
git fetch origin
git reset --hard origin/main
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py migrate
python manage.py fix_boolean_fields
touch passenger_wsgi.py
```

**Time:** 3-5 minutes

**Result:** Admin page will work ✓

---

## After This Fix

Once the admin page works:

1. **Set featured plan** (see `SET_FEATURED_PLAN.md`)
2. **Monitor error logs** in admin
3. **Update production.py and admin.py** for timezone fix (optional, secondary priority)

---

**Status:** Ready to fix - follow commands above ✓
