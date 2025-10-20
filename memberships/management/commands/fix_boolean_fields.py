"""
Django management command to fix boolean field values in database.

Converts string '0' and '1' to proper integer 0 and 1 for BooleanFields.

Usage:
    python manage.py fix_boolean_fields
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix boolean field values in memberships_plan table (convert string to integer)'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.WARNING("Fixing Boolean Fields"))
        self.stdout.write("=" * 60)
        self.stdout.write("")

        with connection.cursor() as cursor:
            # Fix memberships_plan table
            self.stdout.write("Checking memberships_plan table...")
            self.stdout.write("")

            # Show current data
            cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
            rows = cursor.fetchall()

            self.stdout.write(f"Found {len(rows)} plan(s):")
            for row in rows:
                self.stdout.write(f"  ID: {row[0]}, Name: {row[1]}, is_featured: '{row[2]}', is_active: '{row[3]}'")
            self.stdout.write("")

            # Fix is_featured field
            self.stdout.write("Fixing is_featured field...")

            # Set all non-1 values to 0
            cursor.execute("UPDATE memberships_plan SET is_featured = 0 WHERE is_featured != 1;")
            count1 = cursor.rowcount
            self.stdout.write(f"  ✓ Set {count1} row(s) to 0")

            # Ensure 1 values are integers
            cursor.execute("UPDATE memberships_plan SET is_featured = 1 WHERE is_featured = '1';")
            count2 = cursor.rowcount
            if count2 > 0:
                self.stdout.write(f"  ✓ Converted {count2} string '1' to integer 1")

            # Fix is_active field
            self.stdout.write("")
            self.stdout.write("Fixing is_active field...")

            cursor.execute("UPDATE memberships_plan SET is_active = 0 WHERE is_active != 1;")
            count3 = cursor.rowcount
            self.stdout.write(f"  ✓ Set {count3} row(s) to 0")

            cursor.execute("UPDATE memberships_plan SET is_active = 1 WHERE is_active = '1';")
            count4 = cursor.rowcount
            if count4 > 0:
                self.stdout.write(f"  ✓ Converted {count4} string '1' to integer 1")

            # Show fixed data
            self.stdout.write("")
            self.stdout.write("Verifying fix...")
            cursor.execute("SELECT id, name, is_featured, is_active FROM memberships_plan;")
            rows = cursor.fetchall()

            self.stdout.write("")
            self.stdout.write(f"Fixed data ({len(rows)} plan(s)):")
            for row in rows:
                # Check if values are now proper integers
                featured_type = type(row[2]).__name__
                active_type = type(row[3]).__name__
                self.stdout.write(
                    f"  ID: {row[0]}, Name: {row[1]}, "
                    f"is_featured: {row[2]} ({featured_type}), "
                    f"is_active: {row[3]} ({active_type})"
                )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("✓ Boolean fields fixed successfully!"))
        self.stdout.write("=" * 60)
        self.stdout.write("")
        self.stdout.write("Next steps:")
        self.stdout.write("  1. Restart your application:")
        self.stdout.write("     touch passenger_wsgi.py")
        self.stdout.write("")
        self.stdout.write("  2. Test the admin page:")
        self.stdout.write("     https://www.magma7fitness.com/admin/memberships/plan/")
        self.stdout.write("")
