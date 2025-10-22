#!/usr/bin/env python
"""
Import MySQL data into SQLite database.

This script converts the MySQL dump to SQLite format and imports it.
"""

import os
import sys
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.development')
django.setup()

from django.db import connection
from django.core.management import call_command


def convert_mysql_to_sqlite(mysql_file, sqlite_file):
    """Convert MySQL SQL dump to SQLite format"""

    print(f"Reading MySQL dump: {mysql_file}")

    with open(mysql_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    print("Converting MySQL syntax to SQLite...")

    # Remove MySQL-specific syntax
    sql = re.sub(r'ENGINE=\w+', '', sql)
    sql = re.sub(r'DEFAULT CHARSET=\w+', '', sql)
    sql = re.sub(r'COLLATE=[\w_]+', '', sql)
    sql = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql)
    sql = re.sub(r'`', '"', sql)  # Replace backticks with double quotes
    sql = re.sub(r'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql)

    # Remove DROP TABLE IF EXISTS (we'll handle this differently)
    sql = re.sub(r'DROP TABLE IF EXISTS[^;]+;', '', sql)

    # Remove comments
    sql = re.sub(r'--[^\n]*\n', '\n', sql)

    # Write converted SQL
    print(f"Writing SQLite-compatible SQL: {sqlite_file}")
    with open(sqlite_file, 'w', encoding='utf-8') as f:
        f.write(sql)

    print("✓ Conversion complete")
    return sqlite_file


def import_to_sqlite(sql_file):
    """Import SQL file into SQLite database"""

    print("\n" + "="*60)
    print("IMPORTING DATA TO SQLITE")
    print("="*60 + "\n")

    # Read the SQL file
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split into individual statements
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]

    total = len(statements)
    errors = []
    success = 0

    print(f"Found {total} SQL statements to execute\n")

    with connection.cursor() as cursor:
        for i, statement in enumerate(statements, 1):
            if not statement or statement.startswith('--'):
                continue

            try:
                # Skip CREATE TABLE for Django-managed tables
                if statement.strip().upper().startswith('CREATE TABLE'):
                    table_name = re.search(r'CREATE TABLE\s+"?(\w+)"?', statement, re.I)
                    if table_name:
                        print(f"[{i}/{total}] Skipping table creation: {table_name.group(1)}")
                    continue

                # Execute INSERT statements
                if statement.strip().upper().startswith('INSERT'):
                    cursor.execute(statement)
                    success += 1

                    # Show progress every 10 statements
                    if i % 10 == 0:
                        print(f"[{i}/{total}] Processed {success} inserts...")

            except Exception as e:
                error_msg = f"Statement {i}: {str(e)[:100]}"
                errors.append(error_msg)
                # Don't print every error, just count them
                if len(errors) <= 5:
                    print(f"⚠ Warning: {error_msg}")

    print("\n" + "="*60)
    print("IMPORT SUMMARY")
    print("="*60)
    print(f"Total statements: {total}")
    print(f"Successful inserts: {success}")
    print(f"Errors/Skipped: {len(errors)}")

    if errors and len(errors) <= 10:
        print("\nSample errors:")
        for err in errors[:10]:
            print(f"  - {err}")

    print("\n✓ Import complete!")
    return success, len(errors)


def main():
    """Main import process"""

    print("\n" + "="*60)
    print("MYSQL TO SQLITE IMPORT TOOL")
    print("="*60 + "\n")

    mysql_file = 'mysql_import_fixed_20251020_013822.sql'
    sqlite_converted = 'sqlite_import_converted.sql'

    if not os.path.exists(mysql_file):
        print(f"Error: {mysql_file} not found!")
        print("\nAvailable SQL files:")
        for f in os.listdir('.'):
            if f.endswith('.sql'):
                print(f"  - {f}")
        return

    print(f"Input file: {mysql_file}")
    print(f"Database: db.sqlite3")
    print("")

    # Ask for confirmation
    response = input("This will import data into your local SQLite database. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        return

    print("\nStep 1: Converting MySQL dump to SQLite format...")
    sqlite_file = convert_mysql_to_sqlite(mysql_file, sqlite_converted)

    print("\nStep 2: Importing data into SQLite database...")
    success, errors = import_to_sqlite(sqlite_file)

    print("\n" + "="*60)
    print("DONE!")
    print("="*60)
    print(f"\n✓ Imported {success} records")
    if errors > 0:
        print(f"⚠ {errors} errors/warnings (mostly expected)")
    print("\nYou can now run: python manage.py runserver")
    print("")


if __name__ == '__main__':
    main()
