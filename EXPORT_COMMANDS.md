# Quick Database Export Commands

Since you need to export from where Django is installed, run these commands on your server.

---

## Export Database from Server

SSH into your server and run:

```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Export current MySQL database to JSON
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude contenttypes \
    --exclude auth.permission \
    --exclude sessions.session \
    --exclude admin.logentry \
    > database_backup_$(date +%Y%m%d_%H%M%S).json

# Check the file was created
ls -lh database_backup_*.json
```

---

## Download to Local Machine

From your local machine:

```bash
# Download the backup
scp magmafit@yourserver:/home/magmafit/magma7_proj/database_backup_*.json ~/Downloads/

# Or specify exact filename
scp magmafit@yourserver:/home/magmafit/magma7_proj/database_backup_20250120_123456.json ~/Downloads/
```

---

## Create MySQL SQL Dump (Alternative)

If you want a pure SQL dump instead of JSON:

```bash
# On server
mysqldump -u magmafit_dbuser -p magmafit_db > mysql_backup_$(date +%Y%m%d_%H%M%S).sql

# Enter password when prompted

# Check file size
ls -lh mysql_backup_*.sql

# Download to local
scp magmafit@yourserver:/home/magmafit/magma7_proj/mysql_backup_*.sql ~/Downloads/
```

---

## Import to Another Database

### Using JSON (Recommended):

```bash
# On target server
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# First, run migrations
python manage.py migrate

# Then load data
python manage.py loaddata database_backup_20250120_123456.json
```

### Using SQL Dump:

```bash
# Import SQL dump
mysql -u magmafit_dbuser -p magmafit_db < mysql_backup_20250120_123456.sql
```

---

## Backup Specific Apps Only

If you only want to backup certain apps:

```bash
# Backup only users and memberships
python manage.py dumpdata auth.user users memberships > users_memberships_backup.json

# Backup only membership plans
python manage.py dumpdata memberships.plan > plans_backup.json

# Backup payments
python manage.py dumpdata payments > payments_backup.json
```

---

## Quick Backup Script

Create this file on your server: `backup_db.sh`

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/magmafit/backups"
mkdir -p "$BACKUP_DIR"

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate

# Django JSON backup
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude contenttypes \
    --exclude auth.permission \
    --exclude sessions.session \
    > "$BACKUP_DIR/backup_$TIMESTAMP.json"

# MySQL SQL backup
mysqldump -u magmafit_dbuser -p magmafit_db > "$BACKUP_DIR/mysql_$TIMESTAMP.sql"

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.json"
echo "MySQL dump: $BACKUP_DIR/mysql_$TIMESTAMP.sql"
```

Make it executable and run:
```bash
chmod +x backup_db.sh
./backup_db.sh
```

---

## Summary

**Easiest method:**
1. SSH into server
2. Run: `python manage.py dumpdata > backup.json`
3. Download: `scp server:/path/backup.json ~/Downloads/`

**For MySQL SQL dump:**
1. SSH into server
2. Run: `mysqldump -u user -p database > backup.sql`
3. Download: `scp server:/path/backup.sql ~/Downloads/`

Both methods create files you can import to MySQL!
