#!/usr/bin/env python
import os
import sys

# Configure PyMySQL to work as MySQLdb replacement
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

