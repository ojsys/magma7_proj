# Database Migration: SQLite to MySQL

## Overview
This guide will help you export your local SQLite database and import it to MySQL on your cPanel server.

---

## Step 1: Export Database (On Local Machine)

### Option A: Using the Bash Script (Recommended)

```bash
cd /Users/Apple/projects/magma7_proj
chmod +x create_mysql_dump.sh
./create_mysql_dump.sh
```

This will create:
- `database_backup_YYYYMMDD_HHMMSS.json` - Your data export
- `mysql_import_YYYYMMDD_HHMMSS.sql` - Instructions file
- `DATABASE_MIGRATION_README.txt` - Quick reference

### Option B: Using Django Command Directly

```bash
cd /Users/Apple/projects/magma7_proj
source venv/bin/activate

# Export all data to JSON
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude contenttypes \
    --exclude auth.permission \
    --exclude sessions.session \
    > database_backup.json
```

### Option C: Using Python Script

```bash
python export_to_mysql.py
```

---

## Step 2: Upload to Server

Upload the JSON file to your server:

```bash
# Using SCP
scp database_backup_*.json magmafit@yourserver.com:/home/magmafit/magma7_proj/

# Or using SFTP/cPanel File Manager
# Navigate to: /home/magmafit/magma7_proj/
# Upload the JSON file
```

---

## Step 3: Prepare MySQL Database (On Server)

### Via cPanel:

1. **Go to cPanel → MySQL Databases**

2. **Create Database:**
   - Database name: `magmafit_db` (cPanel adds prefix, full name might be `magmafit_magmafit_db`)
   - Note the full database name shown

3. **Create Database User:**
   - Username: `magmafit_dbuser`
   - Password: Generate strong password
   - Note the full username shown

4. **Add User to Database:**
   - Select user and database
   - Grant **ALL PRIVILEGES**
   - Click "Make Changes"

5. **Note Your Credentials:**
   ```
   Database Name: magmafit_magmafit_db (or whatever cPanel shows)
   Database User: magmafit_magmafit_dbuser (or whatever cPanel shows)
   Database Password: [your password]
   Database Host: localhost
   Database Port: 3306
   ```

### Via MySQL Command Line (Advanced):

```sql
CREATE DATABASE magmafit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'magmafit_user'@'localhost' IDENTIFIED BY 'your-strong-password';
GRANT ALL PRIVILEGES ON magmafit_db.* TO 'magmafit_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Step 4: Update .env File (On Server)

SSH into your server:

```bash
ssh magmafit@yourserver.com
cd /home/magmafit/magma7_proj
nano .env
```

Update these lines with your MySQL credentials:

```env
DB_NAME=magmafit_magmafit_db
DB_USER=magmafit_magmafit_dbuser
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 5: Run Migrations (Creates Tables)

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

# Run migrations to create all tables
python manage.py migrate
```

You should see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

---

## Step 6: Import Data

```bash
# Load data from JSON file
python manage.py loaddata database_backup_*.json
```

Or specify the exact filename:
```bash
python manage.py loaddata database_backup_20250120_143022.json
```

You should see:
```
Installed 150 object(s) from 1 fixture(s)
```

### If Import Fails:

Try with verbose output to see what's wrong:
```bash
python manage.py loaddata database_backup_*.json --verbosity=2
```

Common issues:
- **Integrity errors**: Data conflicts with existing data
- **Missing tables**: Run migrations first
- **Database connection**: Check .env credentials

---

## Step 7: Verify Data

Check data was imported correctly:

```bash
# Enter Django shell
python manage.py dbshell
```

In MySQL prompt:
```sql
-- Check users
SELECT COUNT(*) FROM auth_user;
SELECT username, email FROM auth_user;

-- Check membership plans
SELECT * FROM memberships_plan;

-- Check other tables
SHOW TABLES;

-- Exit
exit;
```

Or use Django shell:
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from memberships.models import Plan

print(f"Users: {User.objects.count()}")
print(f"Plans: {Plan.objects.count()}")

# List all users
for user in User.objects.all():
    print(f"  - {user.username} ({user.email})")

# List all plans
for plan in Plan.objects.all():
    print(f"  - {plan.name}: {plan.price}")
```

---

## Step 8: Create Superuser (If Needed)

If you didn't have a superuser in your SQLite database, create one:

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

---

## Step 9: Restart Application

```bash
touch /home/magmafit/magma7_proj/passenger_wsgi.py
```

Or via cPanel:
- Go to "Setup Python App"
- Click "Restart"

---

## Step 10: Test

1. **Visit your site:** `https://www.magma7fitness.com`

2. **Test admin:** `https://www.magma7fitness.com/admin`
   - Login with superuser credentials
   - Check if all data is visible

3. **Check functionality:**
   - User registration
   - Login/logout
   - Membership plans displayed
   - Payments (if configured)

---

## Troubleshooting

### Issue: "No such table" error

**Solution:** Run migrations first
```bash
python manage.py migrate
```

### Issue: "Duplicate entry" or integrity errors

**Solution:** Database already has data. Clear it first:
```bash
# WARNING: This deletes all data!
python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata database_backup_*.json
```

### Issue: Database connection refused

**Solution:** Check .env credentials
```bash
cat .env | grep DB_

# Test connection
python manage.py dbshell
```

### Issue: Some data missing after import

**Solution:** Check what was excluded during export
```bash
# Export specific apps only
python manage.py dumpdata auth users memberships payments > backup.json
```

### Issue: Need to re-import specific app data

```bash
# Export specific app
python manage.py dumpdata memberships > memberships_backup.json

# Import specific app
python manage.py loaddata memberships_backup.json
```

---

## Advanced: Creating SQL Dump (Alternative Method)

If you need actual SQL statements instead of JSON:

### On Local Machine:

```bash
# Install sqlite3-to-mysql (if not installed)
pip install sqlite3-to-mysql

# Convert SQLite to MySQL SQL
sqlite3mysql -f db.sqlite3 -d magmafit_db -u magmafit_user > mysql_dump.sql
```

### On Server:

```bash
mysql -u magmafit_user -p magmafit_db < mysql_dump.sql
```

**Note:** This method is less reliable than using Django's loaddata.

---

## Backup Strategy

### Regular Backups on Server:

Create a backup script:

```bash
#!/bin/bash
# backup_database.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/magmafit/backups"
mkdir -p "$BACKUP_DIR"

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Django JSON backup
python manage.py dumpdata > "$BACKUP_DIR/django_backup_$TIMESTAMP.json"

# MySQL dump
mysqldump -u magmafit_user -p magmafit_db > "$BACKUP_DIR/mysql_backup_$TIMESTAMP.sql"

echo "Backup completed: $TIMESTAMP"
```

### Restore from Backup:

```bash
# Restore from Django JSON
python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata /path/to/backup.json

# Or restore from MySQL dump
mysql -u magmafit_user -p magmafit_db < /path/to/backup.sql
```

---

## Quick Reference Commands

```bash
# Export database
python manage.py dumpdata > backup.json

# Import database
python manage.py loaddata backup.json

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell

# Check migrations
python manage.py showmigrations

# Reset database (careful!)
python manage.py flush
```

---

## Summary Checklist

- [ ] Export SQLite database to JSON
- [ ] Upload JSON file to server
- [ ] Create MySQL database in cPanel
- [ ] Update .env with database credentials
- [ ] Run migrations on server
- [ ] Import data with loaddata
- [ ] Verify data imported correctly
- [ ] Create/test superuser account
- [ ] Restart application
- [ ] Test website functionality

---

## Need Help?

If you encounter issues:
1. Check error messages carefully
2. Verify database credentials in .env
3. Ensure migrations ran successfully
4. Check Django error logs: `tail -f logs/django_errors.log`
5. Try verbose import: `python manage.py loaddata backup.json --verbosity=2`

Good luck with your migration! 🚀
