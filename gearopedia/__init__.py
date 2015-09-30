#!/usr/bin/python
from flask import Flask
#import gearopedia.views

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG', silent=True)

import gearopedia.views

