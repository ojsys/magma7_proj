#!/usr/bin/env python
"""
Fix MySQL charset issues for django_admin_log and other tables.
This script converts tables and columns to utf8mb4 to support all UTF-8 characters.
"""
import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.production')

import django
django.setup()

from django.db import connection


def fix_charset():
    """Convert django_admin_log and all tables to utf8mb4."""

    with connection.cursor() as cursor:
        # Get database name
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"Working on database: {db_name}")
        print("=" * 60)

        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"Found {len(tables)} tables to convert")
        print("=" * 60)

        for table in tables:
            print(f"\nProcessing table: {table}")

            # Check current charset
            cursor.execute(f"""
                SELECT CCSA.character_set_name
                FROM information_schema.`TABLES` T,
                     information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
                WHERE CCSA.collation_name = T.table_collation
                  AND T.table_schema = %s
                  AND T.table_name = %s
            """, [db_name, table])

            result = cursor.fetchone()
            current_charset = result[0] if result else 'unknown'
            print(f"  Current charset: {current_charset}")

            if current_charset != 'utf8mb4':
                # Convert table
                try:
                    print(f"  Converting table to utf8mb4...")
                    cursor.execute(f"""
                        ALTER TABLE `{table}`
                        CONVERT TO CHARACTER SET utf8mb4
                        COLLATE utf8mb4_unicode_ci
                    """)
                    print(f"  ✓ Successfully converted {table}")
                except Exception as e:
                    print(f"  ✗ Error converting {table}: {e}")
            else:
                print(f"  ✓ Already using utf8mb4")

        print("\n" + "=" * 60)
        print("Charset conversion complete!")
        print("=" * 60)


if __name__ == '__main__':
    try:
        fix_charset()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
