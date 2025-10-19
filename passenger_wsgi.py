"""
Passenger WSGI file for cPanel deployment
This file is used by Passenger (the WSGI server used by cPanel) to serve the Django application
"""
import os
import sys

# Configure PyMySQL to work as MySQLdb replacement
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Add your project directory to the sys.path
# IMPORTANT: Update this path to match your cPanel directory structure
# Example: /home/username/magma7fitness.com/magma7
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the parent directory to sys.path (if needed)
parent_dir = os.path.dirname(project_home)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set the DJANGO_SETTINGS_MODULE environment variable to use production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.production')

# Activate virtual environment
# IMPORTANT: Update this path to match your virtualenv location on cPanel
# Example: /home/username/virtualenv/magma7fitness.com/3.9/bin/activate_this.py
VIRTUALENV = os.path.join(parent_dir, 'virtualenv', 'bin', 'activate_this.py')
if os.path.exists(VIRTUALENV):
    exec(open(VIRTUALENV).read(), {'__file__': VIRTUALENV})

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()
