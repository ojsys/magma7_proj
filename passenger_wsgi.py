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

# Get the absolute path to the project directory
# This file should be in: /home/username/magma7_proj/passenger_wsgi.py
project_home = os.path.dirname(os.path.abspath(__file__))

# Add project directory to sys.path so Python can find the magma7 package
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the DJANGO_SETTINGS_MODULE environment variable to use production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magma7.settings.production')

# Activate virtual environment if needed
# cPanel usually handles this automatically when you set up the Python app
# But if you need manual activation, uncomment and update this:
# VIRTUALENV = '/home/username/virtualenv/magma7_proj/3.12/bin/activate_this.py'
# if os.path.exists(VIRTUALENV):
#     exec(open(VIRTUALENV).read(), {'__file__': VIRTUALENV})

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()
