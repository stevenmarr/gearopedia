#!flask/bin/python

# Run a test server.
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

os.environ['APP_CONFIG'] = '%s/config/development.py' % BASE_DIR

from gearopedia import app
app.run(host='127.0.0.1', port=8080, debug=True)
