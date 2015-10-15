#!flask/bin/python

# Run a test server.
import os

os.environ['APP_CONFIG'] = '/var/www/gearopedia/config/development.py'

from gearopedia import app
app.run(host='127.0.0.1', port=8080, debug=True)
