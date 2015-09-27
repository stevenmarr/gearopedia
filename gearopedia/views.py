#!/gearopedia/views.py
import os
import logging

from flask import render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from flask import send_from_directory
from oauth2client import client, crypt

from models import GearCategories, GearModels, Base, UploadedFiles, Images
from forms import AddCategoryForm, ModelForm
from gearopedia import app
from database import db_session as session
from utils import check_login, add_file, delete_files, delete_image, add_image

CLIENT_ID = app.config['CLIENT_ID']
# Handlers****************************************
# Login/Logout Handlers
@app.route('/tokensignin', methods=['POST'])
def tokensignin():
    """verify idtoken then set login_session"""
    token = request.form['idtoken']

    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Login Failed")
    login_session['user_id'] = idinfo['sub']
    login_session['name'] = idinfo['name']
    if idinfo.has_key('picture'):
      login_session['picture'] = idinfo['picture']
    else:
      login_session['picture'] = "https://upload.wikimedia.org/wikipedia/commons/7/70/User_icon_BLACK-01.png"
    response = "Login Success"
    return response


@app.route('/tokensignout', methods=['POST'])
def tokensignout():
    """verify idtoken then del login_session"""
    token = request.form['idtoken']
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Logout Failed")
    del login_session['user_id']
    del login_session['name']
    del login_session['picture']
    response = "Logout Success"
    return response


# Category Handlers
@app.route('/')
def defaultgearcategories():
    """Render home page"""
    categories = session.query(GearCategories).all()
    return render_template('default.html',
                           categories=categories,
                           login_session=login_session,
                           page_title='Categories',
                           CLIENT_ID=CLIENT_ID)


@app.route('/add_category/', methods=['GET', 'POST'])
def addgearcategory():
    """Handler for adding a new gear category"""
    if check_login():
        if request.method == 'POST':
            form = AddCategoryForm(request.form, csrf_context=login_session)
            # Validate form data, re-render form if there are errors
            if not form.validate():
                # render form with errors
                return render_template('add_category.html',
                                       form=form,
                                       login_session=login_session,
                                       CLIENT_ID=CLIENT_ID)
            # Store new category in DB
            new_category = GearCategories(name=form.name.data,
                                          user_id=login_session['name'])
            session.add(new_category)
            session.commit()
            flash('New category added')
            return redirect(url_for('defaultgearcategories'))
        else:  # Handle GET requests
            form = AddCategoryForm(csrf_context=login_session)
            return render_template('add_category.html',
                                   form=form,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID)


@app.route('/delete_category/<int:category_id>/', methods=['GET', 'POST'])
def deletegearcategory(category_id):
    """For a given category_id delete the models and category related to the category_id"""
    if check_login():
        category = \
            session.query(GearCategories).filter_by(id=category_id).one()
        if request.method == 'POST':
            models = \
                session.query(GearModels).filter_by(category=category).all()

            # Deleting a category also deletes the models in the category and files for that model
            for model in models:
                delete_files(model.id)
                delete_image(model.id)
                session.delete(model)
                session.commit()
            session.delete(category)
            session.commit()
            flash('Category %s deleted' % category.name)
            return redirect(url_for('defaultgearcategories'))
        else:

            # Handle GET requests

            return render_template('delete_category.html',
                                   category=category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID, )


# Individual gear model handlers
@app.route('/add_item/<int:category_id>/', methods=['GET', 'POST'])
def addmodel(category_id):
    """For a given category_id add a model"""
    if check_login():
        # Retrieve category from DB
        category = \
            session.query(GearCategories).filter_by(id=category_id).one()
        # Handle POST requests
        if request.method == 'POST':
            # Render form, validate data
            form = ModelForm(request.form, csrf_context=login_session)
            if not form.validate():
                return render_template('model_form.html',
                                       form=form,
                                       category=category,
                                       login_session=login_session,
                                       CLIENT_ID=CLIENT_ID, )
            # create new model object    
            model = GearModels(category=category,
                               user_id=login_session['name'])
            form.populate_obj(model)

            # check for image upload if it exists
            image = request.files['image']
            if image:
                model.image_path = add_image(image, model.id)
            # add model to db
            session.add(model)
            session.commit()
            flash('New model created')
            # check for file upload if one exists
            uploaded_file = request.files['file']
            if uploaded_file:
                try:
                    add_file(uploaded_file, form.file_type.data, model.id, edit=True)
                    flash('File upload successful')
                except TypeError:
                    flash('File type incorrect')
                except OSError:
                    flash('File upload error')
            return redirect(url_for('viewmodels',
                                    category_id=model.category_id))
        else:
            # Handle GET requests
            form = ModelForm(csrf_context=login_session)
            return render_template('model_form.html',
                                   form=form,
                                   category=category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID)


@app.route('/view_items/<int:category_id>/')
def viewmodels(category_id):
    """For a given category_id render a template with all the models in the category"""
    models = \
        session.query(GearModels).filter_by(category_id=category_id).order_by(GearModels.manufacturer).all()
    files = session.query(UploadedFiles).all()
    images = session.query(Images).all()
    return render_template('view_models.html',
                           models=models,
                           category_id=category_id,
                           login_session=login_session,
                           files=files,
                           images=images,
                           CLIENT_ID=CLIENT_ID)


@app.route('/edit_model/<int:model_id>/', methods=['GET', 'POST'])
def editmodel(model_id):
    """Render the model_form page with model to update"""
    if check_login():
        model = session.query(GearModels).filter_by(id=model_id).one()
        if request.method == 'POST':
            form = ModelForm(request.form, csrf_context=login_session)
            # Validate form data
            if not form.validate():
                return render_template('model_form.html',
                                       form=form,
                                       category=model.category,
                                       login_session=login_session,
                                       CLIENT_ID=CLIENT_ID)
            form.populate_obj(model)
            # Retrieve updated image if it exists and upload it
            image = request.files['image']
            if image:
                path = add_image(image, model.id)
                model.image_path = path
            # add model to db
            session.add(model)
            session.commit()
            flash('Model %s edited' % model.name)

            # check for file upload if one exists
            model_file = request.files['file']
            if model_file:
                try:
                    add_file(model_file, form.file_type.data, model.id, edit=True)
                    flash('File upload successful')
                except TypeError:
                    flash('File type incorrect')
                except OSError:
                    flash('File upload error')
            return redirect(url_for('viewmodels',
                                    category_id=model.category_id))
        else:

            # Handle GET requests

            form = ModelForm(obj=model, csrf_context=login_session)
            return render_template('model_form.html',
                                   form=form,
                                   model=model,
                                   category=model.category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID, 
                                   )


@app.route('/delete_model/<int:model_id>/', methods=['GET', 'POST'])
def deletemodel(model_id):
    """For a given model_id delete the model"""

    # Verify user is logged in
    if check_login():
        model = session.query(GearModels).filter_by(id=model_id).one()
        # Handle POST requests
        if request.method == 'POST':
            # Delete from DB
            delete_files(model_id)
            delete_image(model_id)
            session.delete(model)
            session.commit()
            flash('Model %s deleted' % model.name)
            return redirect(url_for('viewmodels',
                                    category_id=model.category_id))
        else:
            # Handle GET requests
            return render_template('delete_model.html',
                                   model=model,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID, )


# File serving handler
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Given a filename return the file"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Image serving handler
@app.route('/images/<filename>')
def uploaded_img(filename):
    """Given a filename return the image"""
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)


# JSON Handler
@app.route('/json/')
def json_call():
    """Return JSON object off all category and model data"""
    models = session.query(GearModels).all()
    return jsonify(AllModels=[model.serialize for model in models])

