#!/usr/bin/env python3
"""
Convert SQLite database to MySQL-compatible SQL dump
Fixed version with proper MySQL syntax
"""

import sqlite3
import re
from datetime import datetime

# Configuration
SQLITE_DB = 'db.sqlite3'
OUTPUT_SQL = f'mysql_import_fixed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'

def convert_sqlite_to_mysql():
    """Convert SQLite database to MySQL SQL dump"""

    print("=" * 70)
    print("SQLite to MySQL Converter (Fixed)")
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
            f.write("-- Magma7 Fitness - MySQL Import File (Fixed)\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- From SQLite database: {SQLITE_DB}\n")
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

                # Get table info
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns_info = cursor.fetchall()

                # Build CREATE TABLE statement
                f.write(f"\n-- Table: {table_name}\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                f.write(f"CREATE TABLE `{table_name}` (\n")

                column_defs = []
                for col in columns_info:
                    col_id, col_name, col_type, not_null, default_val, is_pk = col

                    # Build column definition
                    col_def = f"  `{col_name}` {convert_type(col_type)}"

                    if not_null:
                        col_def += " NOT NULL"

                    if is_pk:
                        col_def += " PRIMARY KEY"
                        if 'int' in col_type.lower() or col_type == '':
                            col_def += " AUTO_INCREMENT"

                    if default_val is not None and not is_pk:
                        col_def += f" DEFAULT {default_val}"

                    column_defs.append(col_def)

                f.write(",\n".join(column_defs))
                f.write("\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n\n")

                # Get data
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                if rows:
                    # Get column names
                    columns = [col[1] for col in columns_info]

                    # Write INSERT statements
                    f.write(f"-- Data for table: {table_name}\n")

                    # Write inserts in batches of 100 for better performance
                    batch_size = 100
                    for batch_start in range(0, len(rows), batch_size):
                        batch_rows = rows[batch_start:batch_start + batch_size]

                        f.write(f"INSERT INTO `{table_name}` (`")
                        f.write("`, `".join(columns))
                        f.write("`) VALUES\n")

                        for i, row in enumerate(batch_rows):
                            values = []
                            for val in row:
                                values.append(escape_value(val))

                            # Add comma for all but last row in batch
                            ending = ',' if i < len(batch_rows) - 1 else ';'
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
        import traceback
        traceback.print_exc()

def convert_type(sqlite_type):
    """Convert SQLite type to MySQL type"""
    sqlite_type = sqlite_type.upper()

    # Handle empty type (SQLite allows this, defaults to numeric)
    if not sqlite_type:
        return 'INTEGER'

    # Integer types
    if 'INT' in sqlite_type:
        if 'TINY' in sqlite_type or 'BOOL' in sqlite_type:
            return 'TINYINT'
        elif 'SMALL' in sqlite_type:
            return 'SMALLINT'
        elif 'MEDIUM' in sqlite_type:
            return 'MEDIUMINT'
        elif 'BIG' in sqlite_type:
            return 'BIGINT'
        else:
            return 'INTEGER'

    # String types
    if 'CHAR' in sqlite_type or 'TEXT' in sqlite_type or 'CLOB' in sqlite_type:
        if 'VARCHAR' in sqlite_type:
            # Extract length if present
            match = re.search(r'\((\d+)\)', sqlite_type)
            if match:
                return f'VARCHAR({match.group(1)})'
            return 'VARCHAR(255)'
        elif 'CHAR' in sqlite_type and 'VARCHAR' not in sqlite_type:
            match = re.search(r'\((\d+)\)', sqlite_type)
            if match:
                return f'CHAR({match.group(1)})'
            return 'CHAR(255)'
        else:
            return 'TEXT'

    # Floating point
    if 'REAL' in sqlite_type or 'FLOA' in sqlite_type or 'DOUB' in sqlite_type:
        return 'DOUBLE'

    if 'DECIMAL' in sqlite_type or 'NUMERIC' in sqlite_type:
        return 'DECIMAL(10,2)'

    # Binary
    if 'BLOB' in sqlite_type:
        return 'BLOB'

    # Date/Time
    if 'DATE' in sqlite_type and 'TIME' in sqlite_type:
        return 'DATETIME'
    elif 'DATE' in sqlite_type:
        return 'DATE'
    elif 'TIME' in sqlite_type:
        return 'TIME'

    # Default
    return 'TEXT'

def escape_value(val):
    """Escape value for SQL"""
    if val is None:
        return 'NULL'
    elif isinstance(val, bool):
        return '1' if val else '0'
    elif isinstance(val, (int, float)):
        return str(val)
    elif isinstance(val, bytes):
        return f"X'{val.hex()}'"
    else:
        # Escape single quotes and backslashes
        escaped = str(val).replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
        return f"'{escaped}'"

if __name__ == '__main__':
    convert_sqlite_to_mysql()
