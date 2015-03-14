from flask import Flask, render_template, url_for, request, redirect, flash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import GearCategories, GearModels, Base

#from wtforms import *

app = Flask(__name__)
engine = create_engine('sqlite:///gear_wiki.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def DefaultGearCategories():
	categories = session.query(GearCategories).all()
	return render_template('default.html', categories=categories)

if __name__ == '__main__':
	app.secret_key = 'super-secret-key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)
