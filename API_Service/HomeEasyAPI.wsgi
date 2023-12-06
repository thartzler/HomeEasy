import sys
import logging
import os

os.environ["AZURE_SQL_CONNECTIONSTRING"] = <REDACTED>

sys.path.insert(0, '/var/www/HomeEasy-API/')
sys.path.insert(0, '/var/www/HomeEasy-API/venv/lib/python3.8/site-packages/')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from api import app as application

