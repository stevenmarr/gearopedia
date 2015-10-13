import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG', silent=True)  # Loads config/production.py when APP_CONFIG is defined

db = SQLAlchemy(app)


import views, models


BASE_DIR = app.config['BASE_DIR']
ADMINS = app.config['ADMINS']
MAIL_SERVER = app.config['MAIL_SERVER']
MAIL_PORT = app.config['MAIL_PORT']
MAIL_USERNAME = app.config['MAIL_USERNAME']
MAIL_PASSWORD = app.config['MAIL_PASSWORD']

if not app.debug:
    # Email errors
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
    	'no-reply@' + MAIL_SERVER, ADMINS, 'gearopedia failure',
    	credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    # Logging
    file_handler = RotatingFileHandler('tmp/gearopedia.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('gearopedia startup')

# create file and image upload folder structure if it does not exist
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
