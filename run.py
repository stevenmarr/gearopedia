#!flask/bin/python

# Run a test server.
import os

os.environ['APP_CONFIG'] = "config.DevelopmentConfig"

from gearopedia import app

app.run()
