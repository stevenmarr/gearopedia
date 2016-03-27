import os
import logging
import sqlalchemy

from flask import render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from flask import send_from_directory
from oauth2client import client, crypt

from .models import GearCategories, GearModels, UploadedFiles, Images
from .forms import AddCategoryForm, ModelForm, LoginForm
from gearopedia import app, db
# import db.db_session as session
from utils import login_required


session = db.session

CLIENT_ID = app.config['CLIENT_ID']

@app.errorhandler(500)
def internal_error(error):
    session.rollback()
    flash('SOMETHING BROKE!')
    return render_template('500.html', login_session=login_session), 500


# File serving handler
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Return the uploaded file URL."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Image serving handler
@app.route('/images/<filename>')
def uploaded_img(filename):
    """Return the uploaded image URL."""
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)




