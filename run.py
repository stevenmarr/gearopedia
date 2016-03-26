#!flask/bin/python

# Run a test server.
import os

# config

#BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#os.environ['APP_CONFIG'] = '%s/config/development.py' % BASE_DIR


from gearopedia import app
app.run()
