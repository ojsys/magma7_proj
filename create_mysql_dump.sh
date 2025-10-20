#!/bin/bash
# Script to export SQLite database and prepare for MySQL import

echo "=========================================="
echo "Magma7 Fitness - Database Export Script"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate || source virtualenv/bin/activate
fi

# Set timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
JSON_FILE="database_backup_${TIMESTAMP}.json"
SQL_FILE="mysql_import_${TIMESTAMP}.sql"

echo "Step 1: Exporting database to JSON..."
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude contenttypes \
    --exclude auth.permission \
    --exclude sessions.session \
    --exclude admin.logentry \
    > "$JSON_FILE"

if [ $? -eq 0 ]; then
    echo "✓ JSON export completed: $JSON_FILE"
else
    echo "✗ Error exporting database"
    exit 1
fi

echo ""
echo "Step 2: Creating MySQL import instructions..."

cat > "$SQL_FILE" << 'EOF'
-- =====================================================
-- Magma7 Fitness - MySQL Database Import Instructions
-- =====================================================
--
-- IMPORTANT: Don't use this SQL file directly!
-- Instead, use Django's loaddata command with the JSON file.
--
-- SETUP STEPS:
-- ============
--
-- 1. CREATE DATABASE (in cPanel or MySQL):
--    CREATE DATABASE magmafit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--    CREATE USER 'magmafit_user'@'localhost' IDENTIFIED BY 'your-password';
--    GRANT ALL PRIVILEGES ON magmafit_db.* TO 'magmafit_user'@'localhost';
--    FLUSH PRIVILEGES;
--
-- 2. UPDATE .env FILE on server:
--    DB_NAME=magmafit_db
--    DB_USER=magmafit_user
--    DB_PASSWORD=your-password
--    DB_HOST=localhost
--    DB_PORT=3306
--
-- 3. RUN MIGRATIONS (creates all tables):
--    cd /home/magmafit/magma7_proj
--    source ~/virtualenv/magma7_proj/3.12/bin/activate
--    export DJANGO_SETTINGS_MODULE=magma7.settings.production
--    python manage.py migrate
--
-- 4. LOAD DATA from JSON file:
EOF

echo "    python manage.py loaddata $JSON_FILE" >> "$SQL_FILE"

cat >> "$SQL_FILE" << 'EOF'
--
-- 5. CREATE SUPERUSER (if needed):
--    python manage.py createsuperuser
--
-- 6. VERIFY DATA:
--    python manage.py dbshell
--    SELECT COUNT(*) FROM auth_user;
--    SELECT * FROM memberships_plan;
--
-- =====================================================
-- Alternative: Direct SQL Import (NOT RECOMMENDED)
-- =====================================================
-- If you absolutely need to use SQL instead of loaddata,
-- you'll need to convert the JSON file to SQL statements.
-- This is complex and error-prone. Use loaddata instead!
--
-- =====================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

-- Tables will be created by: python manage.py migrate
-- Data will be loaded by: python manage.py loaddata

SET FOREIGN_KEY_CHECKS=1;
EOF

echo "✓ SQL instructions file created: $SQL_FILE"

echo ""
echo "Step 3: Creating README..."

cat > "DATABASE_MIGRATION_README.txt" << EOF
========================================
DATABASE MIGRATION TO MYSQL
========================================

Files Created:
--------------
1. $JSON_FILE  (Django data dump - USE THIS!)
2. $SQL_FILE              (Instructions file)

How to Import on Server:
------------------------

1. Upload the JSON file to your server:
   scp $JSON_FILE magmafit@yourserver:/home/magmafit/magma7_proj/

2. SSH into your server:
   ssh magmafit@yourserver

3. Navigate to project directory:
   cd /home/magmafit/magma7_proj

4. Activate virtual environment:
   source ~/virtualenv/magma7_proj/3.12/bin/activate

5. Set production settings:
   export DJANGO_SETTINGS_MODULE=magma7.settings.production

6. Run migrations (creates tables):
   python manage.py migrate

7. Load your data:
   python manage.py loaddata $JSON_FILE

8. Verify data loaded:
   python manage.py dbshell
   SELECT COUNT(*) FROM auth_user;
   SELECT * FROM memberships_plan;
   exit

9. Create a superuser if needed:
   python manage.py createsuperuser

10. Restart application:
    touch passenger_wsgi.py

Done! Your data is now in MySQL.

Troubleshooting:
----------------
If loaddata fails:
- Check database credentials in .env
- Ensure migrations ran successfully
- Check for data integrity issues
- Try loading with: python manage.py loaddata $JSON_FILE --verbosity=2

Need to start fresh?
- Drop all tables: python manage.py flush
- Run migrations again: python manage.py migrate
- Load data again: python manage.py loaddata $JSON_FILE

========================================
Generated: $(date)
========================================
EOF

echo "✓ README created: DATABASE_MIGRATION_README.txt"

echo ""
echo "=========================================="
echo "EXPORT COMPLETED!"
echo "=========================================="
echo ""
echo "Files created:"
echo "  📄 $JSON_FILE"
echo "  📄 $SQL_FILE"
echo "  📄 DATABASE_MIGRATION_README.txt"
echo ""
echo "Next steps:"
echo "  1. Upload $JSON_FILE to your server"
echo "  2. Follow instructions in DATABASE_MIGRATION_README.txt"
echo ""
echo "Quick command to upload:"
echo "  scp $JSON_FILE magmafit@yourserver:/home/magmafit/magma7_proj/"
echo ""
echo "=========================================="
