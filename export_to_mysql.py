#!/usr/bin/env python
"""
Export SQLite database to MySQL-compatible SQL dump
Run this script from your local machine before deploying to production
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.development')

# Initialize Django
django.setup()

from django.core.management import call_command
from django.apps import apps
from datetime import datetime

def export_database():
    """Export database using Django's dumpdata command"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Output files
    json_file = f'database_backup_{timestamp}.json'
    sql_file = f'mysql_import_{timestamp}.sql'

    print("=" * 70)
    print("EXPORTING SQLITE DATABASE TO MYSQL-COMPATIBLE SQL")
    print("=" * 70)
    print()

    # Step 1: Export to JSON
    print(f"Step 1: Exporting database to JSON format...")
    print(f"Output file: {json_file}")

    try:
        with open(json_file, 'w') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--indent', '2',
                '--exclude', 'contenttypes',
                '--exclude', 'auth.permission',
                '--exclude', 'sessions.session',
                stdout=f
            )
        print(f"✓ JSON export completed: {json_file}")
    except Exception as e:
        print(f"✗ Error exporting to JSON: {e}")
        return

    print()

    # Step 2: Create MySQL import instructions
    print(f"Step 2: Creating MySQL import SQL file...")
    print(f"Output file: {sql_file}")

    try:
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- =====================================================\n")
            f.write("-- Magma7 Fitness - MySQL Database Import\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- =====================================================\n\n")

            f.write("-- INSTRUCTIONS:\n")
            f.write("-- 1. Create your MySQL database in cPanel\n")
            f.write("-- 2. Run migrations first: python manage.py migrate\n")
            f.write("-- 3. Then load this data: python manage.py loaddata database_backup_*.json\n")
            f.write("-- 4. Or use this SQL file for manual import\n\n")

            f.write("-- Set character set\n")
            f.write("SET NAMES utf8mb4;\n")
            f.write("SET CHARACTER SET utf8mb4;\n\n")

            f.write("-- Disable foreign key checks during import\n")
            f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

            f.write("-- NOTE: This file is a placeholder.\n")
            f.write("-- Use the JSON file with Django's loaddata command instead.\n")
            f.write("-- Command: python manage.py loaddata database_backup_*.json\n\n")

            f.write("-- Re-enable foreign key checks\n")
            f.write("SET FOREIGN_KEY_CHECKS=1;\n")

        print(f"✓ SQL file created: {sql_file}")
    except Exception as e:
        print(f"✗ Error creating SQL file: {e}")
        return

    print()
    print("=" * 70)
    print("EXPORT COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Files created:")
    print(f"  1. {json_file} - Django data dump (USE THIS)")
    print(f"  2. {sql_file} - SQL instructions file")
    print()
    print("Next steps:")
    print("  1. Upload both files to your server")
    print("  2. On server, run migrations: python manage.py migrate")
    print(f"  3. Load data: python manage.py loaddata {json_file}")
    print()
    print("=" * 70)

if __name__ == '__main__':
    export_database()
