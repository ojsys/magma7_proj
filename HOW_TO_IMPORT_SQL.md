# How to Import SQL File to MySQL in cPanel

## Your SQL File is Ready! ✅

File created: **`mysql_import_20251020_013059.sql`**

This file contains:
- 4 users
- 3 membership plans
- 2 subscriptions
- 6 payments
- All your CMS content (programs, testimonials, services, etc.)
- Total: ~180 rows of data

---

## Method 1: Import via cPanel phpMyAdmin (Easiest)

### Step 1: Upload SQL File

First, upload the SQL file to your server:

**Option A: Via SCP**
```bash
scp mysql_import_20251020_013059.sql magmafit@yourserver:/home/magmafit/magma7_proj/
```

**Option B: Via cPanel File Manager**
1. Log into cPanel
2. Go to File Manager
3. Navigate to `/home/magmafit/magma7_proj/`
4. Click "Upload"
5. Select `mysql_import_20251020_013059.sql`

### Step 2: Import via phpMyAdmin

1. **Login to cPanel**

2. **Find and click "phpMyAdmin"**

3. **Select your database** from the left sidebar
   - Look for: `magmafit_db` or `magmafit_magmafit_db`

4. **Click "Import" tab** at the top

5. **Click "Choose File"** and select: `mysql_import_20251020_013059.sql`

6. **Scroll down and click "Go"** button

7. **Wait for import** - You should see:
   ```
   Import has been successfully finished, X queries executed.
   ```

8. **Verify data** - Click "Browse" on some tables to see your data

---

## Method 2: Import via SSH (Advanced)

If you prefer command line:

```bash
# SSH into your server
ssh magmafit@yourserver

# Navigate to project
cd /home/magmafit/magma7_proj

# Import SQL file
mysql -u magmafit_dbuser -p magmafit_db < mysql_import_20251020_013059.sql

# Enter password when prompted

# Verify
mysql -u magmafit_dbuser -p magmafit_db -e "SELECT COUNT(*) FROM auth_user;"
```

---

## Method 3: Via cPanel MySQL (Alternative)

Some cPanels have a direct MySQL import:

1. Go to cPanel → **"MySQL Databases"**
2. Scroll to **"Import Database"** (if available)
3. Select your database
4. Upload SQL file
5. Click Import

---

## Important: Before Importing

### If Database is Empty (New Setup):

Just import the SQL file - it will create all tables and data!

### If Database Already Has Data:

The SQL file starts with `DROP TABLE IF EXISTS`, so it will:
- ✅ Replace existing tables
- ✅ Delete old data
- ✅ Import fresh data

**⚠️ Backup first if you have data you want to keep!**

To backup existing database:
```bash
mysqldump -u magmafit_dbuser -p magmafit_db > backup_before_import.sql
```

---

## After Import

### Step 1: Verify Data

In phpMyAdmin or MySQL shell:

```sql
-- Check users imported
SELECT COUNT(*) FROM auth_user;
-- Should show: 4

-- Check membership plans
SELECT * FROM memberships_plan;
-- Should show: 3 plans

-- Check subscriptions
SELECT COUNT(*) FROM memberships_subscription;
-- Should show: 2

-- List all tables
SHOW TABLES;
-- Should show: 35 tables
```

### Step 2: Restart Django Application

```bash
# Via SSH
touch /home/magmafit/magma7_proj/passenger_wsgi.py

# Or via cPanel
# Go to: Setup Python App → Restart
```

### Step 3: Test Website

1. Visit: `https://www.magma7fitness.com`
2. Check homepage loads
3. Test admin: `https://www.magma7fitness.com/admin`
4. Login with one of your imported users

---

## Troubleshooting

### Error: "Access denied"

**Fix:** Check database credentials
```bash
nano /home/magmafit/magma7_proj/.env

# Verify:
DB_NAME=magmafit_db
DB_USER=magmafit_dbuser
DB_PASSWORD=correct-password
```

### Error: "Unknown database"

**Fix:** Create database first in cPanel → MySQL Databases

### Error: "Table already exists"

**Fix:** The SQL file has `DROP TABLE IF EXISTS`, but if this fails:
```sql
-- In phpMyAdmin or MySQL shell
DROP DATABASE magmafit_db;
CREATE DATABASE magmafit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Then import again
```

### Import Times Out

**Fix:** Import via SSH instead of phpMyAdmin
```bash
mysql -u user -p database < file.sql
```

Or increase PHP timeout in cPanel → MultiPHP INI Editor:
- `max_execution_time = 300`
- `upload_max_filesize = 50M`

### Foreign Key Errors

The SQL file disables foreign key checks, but if you still get errors:
```sql
SET FOREIGN_KEY_CHECKS=0;
SOURCE mysql_import_20251020_013059.sql;
SET FOREIGN_KEY_CHECKS=1;
```

---

## File Size

```bash
# Check SQL file size
ls -lh mysql_import_20251020_013059.sql

# If over 50MB, compress it:
gzip mysql_import_20251020_013059.sql
# Creates: mysql_import_20251020_013059.sql.gz

# MySQL can import compressed files:
zcat mysql_import_20251020_013059.sql.gz | mysql -u user -p database
```

---

## Your Imported Data

After import, you'll have:

**Users (4):**
- Login to admin and check Users section

**Membership Plans (3):**
- Should be visible on your pricing page

**Subscriptions (2):**
- Active member subscriptions

**Payments (6):**
- Payment history

**CMS Content:**
- Programs (4)
- Services (3)
- Testimonials (2)
- Hero slides (5)
- About page content
- And more...

---

## Quick Steps Summary

1. ✅ Upload `mysql_import_20251020_013059.sql` to server
2. ✅ Go to cPanel → phpMyAdmin
3. ✅ Select your database
4. ✅ Click Import → Choose File
5. ✅ Select SQL file → Click Go
6. ✅ Wait for success message
7. ✅ Restart Django app
8. ✅ Test your website

**Done!** Your SQLite data is now in MySQL! 🎉

---

## Need to Re-export?

If you make changes and need a fresh SQL file:

```bash
cd /Users/Apple/projects/magma7_proj
python3 sqlite_to_mysql.py
```

This will create a new timestamped SQL file.
