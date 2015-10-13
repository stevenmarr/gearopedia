import os
import logging

from flask import render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from flask import send_from_directory
from oauth2client import client, crypt

from .models import GearCategories, GearModels, UploadedFiles, Images
from .forms import AddCategoryForm, ModelForm, LoginForm
from gearopedia import app, db
# import db.db_session as session
from utils import check_login, add_file, delete_files, delete_image, add_image
session = db.session

CLIENT_ID = app.config['CLIENT_ID']


# Login/Logout Handlers
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user using OpenID"""
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/')
    return render_template('login.html', 
                           login_session=login_session,
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/tokensignin', methods=['POST'])
def tokensignin():
    """Login user if valid id_token exists in request."""
    token = request.form['idtoken']
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Login Failed")
    login_session['user_id'] = idinfo['sub']
    login_session['name'] = idinfo['name']
    if 'picture' in idinfo:
        login_session['picture'] = idinfo['picture']
    else:
        login_session['picture'] = "https://upload.wikimedia.org/wikipedia/commons/7/70/User_icon_BLACK-01.png"
    response = "Login Success"
    return response


@app.route('/tokensignout', methods=['POST'])
def tokensignout():
    """Logout user if valid id_token exists in request."""
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
    session.close()
    return response

# Error Handlers

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', login_session=login_session), 404

@app.errorhandler(500)
def internal_error(error):
    session.rollback()
    return render_template('500.html', login_session=login_session), 500


# Category Handlers
@app.route('/')
def default():
    """Render home page."""
    categories = session.query(GearCategories).all()
    return render_template('default.html',
                           categories=categories,
                           login_session=login_session,
                           page_title='Categories',
                           CLIENT_ID=CLIENT_ID)


@app.route('/add_category/', methods=['GET', 'POST'])
def addgearcategory():
    """Create a new gear category."""
    if check_login():
        if request.method == 'POST':
            form = AddCategoryForm(request.form, )
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
            return redirect(url_for('default'))
        else:  # Handle GET requests
            form = AddCategoryForm()
            return render_template('add_category.html',
                                   form=form,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID)


@app.route('/delete_category/<int:category_id>/', methods=['GET', 'POST'])
def deletegearcategory(category_id):
    """Delete a gear category."""
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
            return redirect(url_for('default'))
        else:

            # Handle GET requests

            return render_template('delete_category.html',
                                   category=category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID, )


# Individual gear model handlers
@app.route('/add_item/<int:category_id>/', methods=['GET', 'POST'])
def addmodel(category_id):
    """Create a new gear model."""
    if check_login():
        # Retrieve category from DB
        category = \
            session.query(GearCategories).filter_by(id=category_id).one()
        # Handle POST requests
        if request.method == 'POST':
            # Render form, validate data
            form = ModelForm(request.form)
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
            form = ModelForm()
            return render_template('model_form.html',
                                   form=form,
                                   category=category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID)


@app.route('/view_items/<int:category_id>/')
def viewmodels(category_id):
    """View all models for a given category."""
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
    """Edit a gear model."""
    if check_login():
        model = session.query(GearModels).filter_by(id=model_id).one()
        if request.method == 'POST':
            form = ModelForm(request.form, )
            # Validate form data
            if not form.validate():
                return render_template('model_form.html',
                                       form=form,
                                       model=model,
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

            form = ModelForm(obj=model, )
            return render_template('model_form.html',
                                   form=form,
                                   model=model,
                                   category=model.category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID, 
                                   )


@app.route('/delete_model/<int:model_id>/', methods=['GET', 'POST'])
def deletemodel(model_id):
    """Delete a gear model."""

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
    """Return the uploaded file URL."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Image serving handler
@app.route('/images/<filename>')
def uploaded_img(filename):
    """Return the uploaded image URL."""
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)


# JSON Handler
@app.route('/json/')
def json_call():
    """Return JSON object off all categories and gear models."""
    models = session.query(GearModels).all()
    return jsonify(AllModels=[model.serialize for model in models])

