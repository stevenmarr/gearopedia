#!/usr/bin/python
from flask import Flask

from flask_wtf.csrf import CsrfProtect


app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
if __name__ == "__main__":
    app.config.from_pyfile('config.py') 

from gearopedia import views
