#!/usr/bin/env python
"""
Extract INSERT statements from MySQL dump and convert to Django loaddata format.
This creates a JSON fixture that can be imported with `python manage.py loaddata`.
"""

import re
import json
import sys


def parse_mysql_insert(insert_statement):
    """Parse MySQL INSERT statement and extract data"""

    # Extract table name
    table_match = re.search(r'INSERT INTO [`"]?(\w+)[`"]?\s*\(([^)]+)\)\s*VALUES\s*(.+)', insert_statement, re.IGNORECASE)
    if not table_match:
        return None

    table_name = table_match.group(1)
    columns = [c.strip().strip('`"') for c in table_match.group(2).split(',')]
    values_str = table_match.group(3)

    # Parse multiple value sets
    # This regex handles values like: (1, 'text', NULL), (2, 'other', 123)
    value_sets = re.findall(r'\(([^)]+)\)', values_str)

    records = []
    for value_set in value_sets:
        # Split values while respecting quoted strings
        values = []
        current = ''
        in_quotes = False
        quote_char = None

        for char in value_set + ',':
            if char in ('"', "'") and (not in_quotes or char == quote_char):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                else:
                    in_quotes = False
                    quote_char = None
            elif char == ',' and not in_quotes:
                values.append(current.strip())
                current = ''
                continue
            current += char

        # Create record dictionary
        record = {}
        for col, val in zip(columns, values):
            # Clean up value
            val = val.strip()

            # Handle NULL
            if val.upper() == 'NULL':
                record[col] = None
            # Handle quoted strings
            elif val.startswith(("'", '"')) and val.endswith(("'", '"')):
                record[col] = val[1:-1].replace("\\'", "'").replace('\\"', '"')
            # Handle numbers
            elif val.isdigit():
                record[col] = int(val)
            else:
                try:
                    record[col] = float(val)
                except:
                    record[col] = val

        records.append((table_name, record))

    return records


def extract_data_from_mysql_dump(mysql_file):
    """Extract all data from MySQL dump file"""

    print(f"Reading: {mysql_file}")

    with open(mysql_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all INSERT statements
    insert_statements = re.findall(r'INSERT INTO[^;]+;', content, re.IGNORECASE | re.MULTILINE | re.DOTALL)

    print(f"Found {len(insert_statements)} INSERT statements")

    all_records = []

    for stmt in insert_statements:
        records = parse_mysql_insert(stmt)
        if records:
            all_records.extend(records)

    print(f"Extracted {len(all_records)} records")

    return all_records


def records_to_django_fixture(records):
    """Convert extracted records to Django fixture format"""

    # Map MySQL table names to Django models
    table_to_model = {
        'memberships_plan': 'memberships.plan',
        'memberships_planfeature': 'memberships.planfeature',
        'cms_sitesettings': 'cms.sitesettings',
        'cms_heroslide': 'cms.heroslide',
        'cms_program': 'cms.program',
        'cms_service': 'cms.service',
        'cms_partner': 'cms.partner',
        'cms_testimonial': 'cms.testimonial',
        'cms_aboutpage': 'cms.aboutpage',
        'cms_corevalue': 'cms.corevalue',
        'cms_whychooseusitem': 'cms.whychooseusitem',
        'cms_aboutgalleryimage': 'cms.aboutgalleryimage',
        'cms_aboutstatistic': 'cms.aboutstatistic',
        'cms_facility': 'cms.facility',
        'cms_teammember': 'cms.teammember',
        'cms_facilitiespage': 'cms.facilitiespage',
        'cms_teampage': 'cms.teampage',
        'cms_richpage': 'cms.richpage',
        'cms_mediaasset': 'cms.mediaasset',
        'cms_homegalleryimage': 'cms.homegalleryimage',
    }

    fixtures = []

    for table_name, record in records:
        if table_name not in table_to_model:
            continue  # Skip tables we don't need

        # Extract pk
        pk = record.pop('id', None)

        # Create fixture object
        fixture = {
            'model': table_to_model[table_name],
            'pk': pk,
            'fields': record
        }

        fixtures.append(fixture)

    print(f"Created {len(fixtures)} fixture objects")

    return fixtures


def main():
    """Main extraction process"""

    print("\n" + "="*60)
    print("MYSQL DUMP TO DJANGO FIXTURE CONVERTER")
    print("="*60 + "\n")

    mysql_file = 'mysql_import_fixed_20251020_013822.sql'
    output_file = 'production_data.json'

    print(f"Input: {mysql_file}")
    print(f"Output: {output_file}")
    print("")

    # Extract records
    print("\nStep 1: Extracting data from MySQL dump...")
    records = extract_data_from_mysql_dump(mysql_file)

    # Convert to Django fixtures
    print("\nStep 2: Converting to Django fixture format...")
    fixtures = records_to_django_fixture(records)

    # Write JSON file
    print(f"\nStep 3: Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print("✓ DONE!")
    print("="*60)
    print(f"\nCreated: {output_file}")
    print(f"Records: {len(fixtures)}")
    print("\nTo import:")
    print(f"  python manage.py loaddata {output_file}")
    print("")


if __name__ == '__main__':
    main()
