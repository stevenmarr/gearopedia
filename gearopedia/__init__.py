import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG', silent=True)  # Loads config/production.py when APP_CONFIG is defined

db = SQLAlchemy(app)

import views, models

BASE_DIR = app.config['BASE_DIR']
img_path = "%s/files/img" % BASE_DIR
try: 
    os.makedirs(img_path)
except OSError:
    if not os.path.isdir(img_path):
        raise

u_path = "%s/files/uploads" % BASE_DIR
try:
    os.makedirs(u_path)
except OSError:
    if not os.path.isdir(u_path):
        raise        

# import gearopedia.views
# from database import init_db

# init_db()
