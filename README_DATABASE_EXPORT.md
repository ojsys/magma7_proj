# Database Export & Import Guide

## Current Situation

You want to create a database dump that can be imported to MySQL on your cPanel server.

---

## ✅ Files Created for You

I've created several tools to help:

1. **`create_mysql_dump.sh`** - Automated export script (run on local if Django installed)
2. **`export_to_mysql.py`** - Python export script
3. **`IMPORT_DATABASE.md`** - Complete migration guide
4. **`EXPORT_COMMANDS.md`** - Quick commands reference
5. **This file** - Quick start guide

---

## 🚀 Quick Start (2 Options)

### Option 1: Export from Your Server (Easiest)

Since Django is already running on your server:

**Step 1: Create backup on server**
```bash
ssh magmafit@yourserver
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Export to JSON
python manage.py dumpdata \
    --natural-foreign \
    --indent 2 \
    --exclude contenttypes \
    --exclude sessions \
    > database_backup.json

# Check file created
ls -lh database_backup.json
```

**Step 2: Download to your computer (optional)**
```bash
# On your local machine
scp magmafit@yourserver:/home/magmafit/magma7_proj/database_backup.json ~/Downloads/
```

**Step 3: Keep backup safe**
The JSON file can be imported back anytime with:
```bash
python manage.py loaddata database_backup.json
```

---

### Option 2: Create MySQL SQL Dump (Alternative)

For a pure SQL dump instead of JSON:

```bash
# On server
ssh magmafit@yourserver

# Dump MySQL database
mysqldump -u magmafit_dbuser -p magmafit_db > mysql_dump.sql

# Download to local
scp magmafit@yourserver:mysql_dump.sql ~/Downloads/
```

---

## 📥 How to Import

### Import JSON Backup:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# First run migrations if needed
python manage.py migrate

# Then load data
python manage.py loaddata database_backup.json
```

### Import SQL Dump:

```bash
mysql -u magmafit_dbuser -p magmafit_db < mysql_dump.sql
```

---

## 🔄 Complete Migration Workflow

If you're migrating to a NEW database:

**1. Create new MySQL database** (in cPanel)
  - Database name: `magmafit_newdb`
  - Create user and grant privileges

**2. Update .env** with new database credentials

**3. Run migrations** (creates tables)
```bash
python manage.py migrate
```

**4. Import data**
```bash
python manage.py loaddata database_backup.json
```

**5. Verify**
```bash
python manage.py dbshell
SELECT COUNT(*) FROM auth_user;
```

**6. Restart app**
```bash
touch passenger_wsgi.py
```

---

## 📚 Detailed Guides

- **`IMPORT_DATABASE.md`** - Complete step-by-step migration guide
- **`EXPORT_COMMANDS.md`** - All export/import commands
- **`create_mysql_dump.sh`** - Automated backup script

---

## ⚡ Quick Commands Reference

```bash
# Export database to JSON
python manage.py dumpdata > backup.json

# Import from JSON
python manage.py loaddata backup.json

# MySQL dump
mysqldump -u user -p database > dump.sql

# MySQL import
mysql -u user -p database < dump.sql

# Check what's in database
python manage.py dbshell
SHOW TABLES;
SELECT COUNT(*) FROM auth_user;

# List all backups
ls -lh *.json *.sql
```

---

## 🎯 What You Need to Do Now

### Simplest Path:

1. **SSH into your server**
   ```bash
   ssh magmafit@yourserver
   ```

2. **Navigate to project**
   ```bash
   cd /home/magmafit/magma7_proj
   source ~/virtualenv/magma7_proj/3.12/bin/activate
   ```

3. **Create backup**
   ```bash
   python manage.py dumpdata --indent 2 > database_backup_$(date +%Y%m%d).json
   ```

4. **Download it** (from your local machine)
   ```bash
   scp magmafit@yourserver:/home/magmafit/magma7_proj/database_backup_*.json ~/Downloads/
   ```

Done! You now have a MySQL-compatible backup file.

---

## ❓ FAQ

**Q: JSON or SQL dump?**
A: Use JSON with `loaddata` - it's the Django way and handles relationships correctly.

**Q: Will this work with MySQL?**
A: Yes! Django's dumpdata/loaddata works across all database backends.

**Q: What if I want to migrate to a different server?**
A: Export JSON, upload to new server, run migrations, then loaddata.

**Q: Can I schedule automatic backups?**
A: Yes! Create a cron job running the backup script daily.

**Q: What gets excluded?**
A: Sessions, permissions (regenerated), contenttypes (auto-created)

---

## 🛟 Need Help?

1. **For export issues**: Check `EXPORT_COMMANDS.md`
2. **For import issues**: Check `IMPORT_DATABASE.md`
3. **For migration**: Follow complete guide in `IMPORT_DATABASE.md`

---

## 🎉 Summary

You have everything you need:
- ✅ Export scripts ready
- ✅ Import commands documented
- ✅ Migration guide complete
- ✅ Troubleshooting included

Just run the export command on your server and you're done!
