#!/usr/bin/env python3
"""
Convert SQLite database to MySQL-compatible SQL dump
This creates a .sql file you can import directly into MySQL via cPanel
"""

import sqlite3
import re
from datetime import datetime

# Configuration
SQLITE_DB = 'db.sqlite3'
OUTPUT_SQL = f'mysql_import_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'

def convert_sqlite_to_mysql():
    """Convert SQLite database to MySQL SQL dump"""

    print("=" * 70)
    print("SQLite to MySQL Converter")
    print("=" * 70)
    print()

    try:
        # Connect to SQLite database
        print(f"Opening SQLite database: {SQLITE_DB}")
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()

        # Open output file
        print(f"Creating MySQL SQL file: {OUTPUT_SQL}")
        with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
            # Write header
            f.write("-- =====================================================\n")
            f.write("-- Magma7 Fitness - MySQL Import File\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- From SQLite database: {}\n".format(SQLITE_DB))
            f.write("-- =====================================================\n\n")

            f.write("SET NAMES utf8mb4;\n")
            f.write("SET CHARACTER SET utf8mb4;\n")
            f.write("SET FOREIGN_KEY_CHECKS=0;\n")
            f.write("SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n\n")

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()

            print(f"\nFound {len(tables)} tables to export\n")

            for (table_name,) in tables:
                # Skip Django internal tables that regenerate
                if table_name in ['django_migrations', 'django_session', 'django_admin_log']:
                    print(f"  Skipping: {table_name}")
                    continue

                print(f"  Exporting: {table_name}...")

                # Get table schema
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                create_table_sql = cursor.fetchone()[0]

                # Convert SQLite CREATE TABLE to MySQL
                mysql_create = convert_create_table(create_table_sql, table_name)
                f.write(f"\n-- Table: {table_name}\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                f.write(mysql_create + "\n\n")

                # Get data
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                if rows:
                    # Get column names
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = [col[1] for col in cursor.fetchall()]

                    # Write INSERT statements
                    f.write(f"-- Data for table: {table_name}\n")
                    f.write(f"INSERT INTO `{table_name}` ({', '.join(['`' + col + '`' for col in columns])}) VALUES\n")

                    for i, row in enumerate(rows):
                        values = []
                        for val in row:
                            if val is None:
                                values.append('NULL')
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            elif isinstance(val, bytes):
                                values.append(f"X'{val.hex()}'")
                            else:
                                # Escape single quotes and backslashes
                                escaped = str(val).replace('\\', '\\\\').replace("'", "\\'")
                                values.append(f"'{escaped}'")

                        # Add comma for all but last row
                        ending = ',' if i < len(rows) - 1 else ';'
                        f.write(f"({', '.join(values)}){ending}\n")

                    f.write("\n")
                    print(f"    ✓ {len(rows)} rows exported")
                else:
                    print(f"    - No data")

            # Write footer
            f.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
            f.write("\n-- Import completed\n")

        conn.close()

        print()
        print("=" * 70)
        print("CONVERSION COMPLETED!")
        print("=" * 70)
        print()
        print(f"MySQL SQL file created: {OUTPUT_SQL}")
        print()
        print("How to import in cPanel:")
        print("  1. Go to cPanel → phpMyAdmin")
        print("  2. Select your database (e.g., magmafit_db)")
        print(f"  3. Click 'Import' tab")
        print(f"  4. Choose file: {OUTPUT_SQL}")
        print("  5. Click 'Go'")
        print()
        print("Or via command line:")
        print(f"  mysql -u your_user -p your_database < {OUTPUT_SQL}")
        print()
        print("=" * 70)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def convert_create_table(sqlite_sql, table_name):
    """Convert SQLite CREATE TABLE to MySQL syntax"""

    # Start with basic conversion
    mysql_sql = sqlite_sql

    # Replace AUTOINCREMENT with AUTO_INCREMENT
    mysql_sql = re.sub(r'AUTOINCREMENT', 'AUTO_INCREMENT', mysql_sql, flags=re.IGNORECASE)

    # Convert data types
    mysql_sql = re.sub(r'\bINTEGER\b', 'INT', mysql_sql, flags=re.IGNORECASE)
    mysql_sql = re.sub(r'\bREAL\b', 'DOUBLE', mysql_sql, flags=re.IGNORECASE)
    mysql_sql = re.sub(r'\bTEXT\b', 'TEXT', mysql_sql, flags=re.IGNORECASE)
    mysql_sql = re.sub(r'\bBLOB\b', 'BLOB', mysql_sql, flags=re.IGNORECASE)

    # Handle datetime fields
    mysql_sql = re.sub(r'datetime\s+NOT NULL', 'DATETIME NOT NULL', mysql_sql, flags=re.IGNORECASE)
    mysql_sql = re.sub(r'datetime\s+NULL', 'DATETIME NULL', mysql_sql, flags=re.IGNORECASE)

    # Add ENGINE and CHARSET
    mysql_sql = re.sub(r'\);?\s*$', '', mysql_sql)
    mysql_sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

    # Wrap table name in backticks
    mysql_sql = re.sub(rf'CREATE TABLE\s+["\']?{table_name}["\']?',
                       f'CREATE TABLE `{table_name}`',
                       mysql_sql,
                       flags=re.IGNORECASE)

    return mysql_sql

if __name__ == '__main__':
    convert_sqlite_to_mysql()
