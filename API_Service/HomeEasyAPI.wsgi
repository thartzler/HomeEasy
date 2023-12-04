import sys
import logging

sys.path.insert(0, '/var/www/HomeEasy-API/')
sys.path.insert(0, '/var/www/HomeEasy-API/venv/lib/python3.8/site-packages/')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from app import app as application

