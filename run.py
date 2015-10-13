#!flask/bin/python

# Run a test server.
from gearopedia import app
app.run(host='127.0.0.1', port=8080, debug=True)
