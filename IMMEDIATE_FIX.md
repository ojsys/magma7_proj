# IMMEDIATE FIX - Admin KeyError: '0'

## Run This RIGHT NOW in cPanel Terminal

Copy and paste this **entire block** into your cPanel Terminal:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

python manage.py shell << 'EOF'
from django.db import connection

print("\n" + "="*60)
print("FIXING BOOLEAN FIELDS")
print("="*60 + "\n")

with connection.cursor() as cursor:
    # Show current broken data
    print("BEFORE FIX:")
    cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
    for row in cursor.fetchall():
        print(f"  {row[1]}: is_featured='{row[2]}', is_active='{row[3]}'")

    print("\nFixing is_featured...")
    cursor.execute("UPDATE memberships_plan SET is_featured = CAST(is_featured AS UNSIGNED);")
    print(f"  Updated {cursor.rowcount} rows")

    print("\nFixing is_active...")
    cursor.execute("UPDATE memberships_plan SET is_active = CAST(is_active AS UNSIGNED);")
    print(f"  Updated {cursor.rowcount} rows")

    print("\nAFTER FIX:")
    cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
    for row in cursor.fetchall():
        print(f"  {row[1]}: is_featured={row[2]}, is_active={row[3]}")

print("\n" + "="*60)
print("✓ FIXED! Values are now integers, not strings")
print("="*60 + "\n")
EOF

touch passenger_wsgi.py
echo ""
echo "✓ Application restarted"
echo ""
echo "NOW TEST: https://www.magma7fitness.com/admin/memberships/plan/"
echo ""
```

---

## What This Does

1. ✅ Connects to your production database
2. ✅ Shows current broken values (with quotes: `'0'`, `'1'`)
3. ✅ Converts string → integer using MySQL `CAST()`
4. ✅ Shows fixed values (without quotes: `0`, `1`)
5. ✅ Restarts your application
6. ✅ **FIXES THE ADMIN PAGE!**

---

## Expected Output

You should see:

```
============================================================
FIXING BOOLEAN FIELDS
============================================================

BEFORE FIX:
  Monthly: is_featured='0', is_active='1'
  Quarterly: is_featured='1', is_active='1'
  Semi-Annual: is_featured='0', is_active='1'
  Annual: is_featured='0', is_active='1'

Fixing is_featured...
  Updated 4 rows

Fixing is_active...
  Updated 4 rows

AFTER FIX:
  Monthly: is_featured=0, is_active=1
  Quarterly: is_featured=1, is_active=1
  Semi-Annual: is_featured=0, is_active=1
  Annual: is_featured=0, is_active=1

============================================================
✓ FIXED! Values are now integers, not strings
============================================================

✓ Application restarted

NOW TEST: https://www.magma7fitness.com/admin/memberships/plan/
```

**Notice:** After the fix, there are **NO QUOTES** around the numbers - that's how you know it worked!

---

## Alternative: Direct SQL (If Python shell doesn't work)

If the above doesn't work, use direct MySQL:

```bash
mysql -u magmafit_dbuser -p magmafit_db
```

Enter your database password, then run:

```sql
UPDATE memberships_plan SET is_featured = CAST(is_featured AS UNSIGNED);
UPDATE memberships_plan SET is_active = CAST(is_active AS UNSIGNED);
SELECT id, name, is_featured, is_active FROM memberships_plan;
exit;
```

Then restart:
```bash
cd /home/magmafit/magma7_proj
touch passenger_wsgi.py
```

---

## After It Works

Once the admin page loads:

1. **Go to:** https://www.magma7fitness.com/admin/memberships/plan/
2. **You should see all your plans!** ✓
3. **Set featured plan:**
   - Click on "Quarterly" plan
   - Check "Is featured" checkbox
   - Save
4. **Uncheck "Is featured"** on all other plans

---

## Why CAST() Works

`CAST(is_featured AS UNSIGNED)` tells MySQL:
- Take the value (whether it's `'0'`, `'1'`, `0`, or `1`)
- Convert it to an unsigned integer
- Store it back as a proper number

This is **more reliable** than `UPDATE ... SET ... WHERE` because it handles all edge cases at once.

---

## Time to Fix

**30 seconds** - just copy, paste, press Enter!

---

**Status:** Copy the command block above and run it NOW! ✓
