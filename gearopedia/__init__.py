from flask import Flask
from flash.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG', silent=True)  # Loads config/production.py when APP_CONFIG is defined

db = SQLAlchemy(app)

from gearopedia import views, models
# import gearopedia.views
# from database import init_db

# init_db()
