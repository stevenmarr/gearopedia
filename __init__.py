#!/usr/bin/python


from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from flask import make_response
from flask import send_from_directory
from werkzeug import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client import client, crypt

from models import GearCategories, GearModels, Base, UploadedFiles, Images

from setting import FILE_TYPE, CLIENT_ID, APPLICATION_NAME, UPLOAD_FOLDER, UPLOAD_IMG_FOLDER, ALLOWED_EXTENSIONS, ALLOWED_IMG_EXTENSIONS, DATA_BASE, SECRET_KEY

from forms import AddCategoryForm, ModelForm

import random
import string
import httplib2
import json
import requests
import os
import logging

app = Flask(__name__)
engine = create_engine(DATA_BASE)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#file helper functions
def allowed_file(filename):
    """Return filename if extension is in ALLOWED_EXTENSIONS"""

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def add_file(upload_file, file_type, model_id, edit=None):
    """given a file, a file type and a model id place the file in the database, replacing existing file_types.
    ........Return the path to the new file"""
    
    # Query existing files
    if edit:    
        model_files = \
            session.query(UploadedFiles).filter_by(model_id=model_id)
    map(delete_file, [model_file.id for model_file in model_files if model_file.file_type == FILE_TYPE[file_type]])

    # Create a secure filename
    if not  allowed_file(upload_file.filename): raise TypeError
    filename = secure_filename(upload_file.filename)
    if not filename: raise TypeError

    # Save file
    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create new UploadedFiles object
    model_file = UploadedFiles()

    # Populate fields
    model_file.file_name = filename
    model_file.file_type = FILE_TYPE[file_type]
    model_file.model_id = model_id
    model_file.user_id = login_session['user_id']
    model_file.path = url_for('uploaded_file', filename=filename)

    # Add to DB
    session.add(model_file)
    session.commit()
    return model_file.path


def delete_file(id):
    """For a given file id delete the file"""
    uploaded_file = session.query(UploadedFiles).filter_by(id=id).one()
    session.delete(uploaded_file)
    session.commit()   
    try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.file_name))
    except: logging.error("File does not exist")

def delete_files(model_id):
    """for a given model_id, delete all its files"""
    try: 
        files = \
                session.query(UploadedFiles).filter_by(model_id=model_id)
        if files:
            map(delete_file, [f.id for f in files])
    except: 
        logging.info("No files exist for deletion")
    

#image helper functions
def allowed_image(filename):
    """Return filename if extension is in ALLOWED_IMG_EXTENSIONS"""

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS


def add_image(upload_image, model_id):
    """Given an upload_image and model_id, assign the upload_image to the model"""
    #Erase existing upload_image if it exists
    model = session.query(GearModels).filter_by(id=model_id)
    delete_image(model_id)

    if not allowed_image(upload_image.filename): raise TypeError
    filename = secure_filename(upload_image.filename)
    if not filename: raise TypeError

    # Save file
    upload_image.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
    path = url_for('uploaded_img', filename=filename)
    # Create new UploadedFiles object
    image = Images(
        file_name = filename,
        model_id = model_id,
        user_id = login_session['name'],
        path = path)
    session.add(image)
    session.commit()

    return path

def delete_image(model_id):
    """Given a model_id erase the stored image"""
    try: 
        image = session.query(Images).filter_by(model_id=model_id).one()
        if image:
            try: 
                os.remove(os.path.join(app.config['UPLOAD_IMG_FOLDER'], image.file_name))       
            except: 
                logging.info("File did not exist")
            session.delete(image)
            session.commit() 
    except: 
        logging.info("No images exist")
        

#login check
def check_login():
    if 'name' not in login_session:
        raise TypeError
    else: return True

#Handlers****************************************

#Login/Logout Handlers
@app.route('/tokensignin', methods=['POST'])
def tokensignin():
    token = request.form['idtoken']
   
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)      
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Login Failed")
    login_session['user_id']  = idinfo['sub']
    login_session['name'] = idinfo['name']
    login_session['picture'] = idinfo['picture']
    response = "<h1> Login Success </h1>"
    return response


@app.route('/tokensignout', methods=['POST'])
def tokensignout():
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
    response = "<h1> Logout Success </h1>"
    return response


#Category Handlers
@app.route('/')
def defaultgearcategories():
    """Render home page"""
    categories = session.query(GearCategories).all()
    return render_template('default.html', categories=categories,
                           login_session=login_session,
                           page_title='Categories',
			   CLIENT_ID=CLIENT_ID, )


@app.route('/add_category/', methods=['GET', 'POST'])
def addgearcategory():
    """Handler for adding a new gear category"""
    if check_login():
        if request.method == 'POST':
            form = AddCategoryForm(request.form)
            # Validate form data, re-render form if there are erros
            if not form.validate():
                # render form with errors
                return render_template('add_category.html', 
					form=form,
					CLIENT_ID=CLIENT_ID, )
            # Store new category in DB
            new_category = GearCategories(name=form.name.data,
                                          user_id=login_session['user_id'])
            session.add(new_category)
            session.commit()
            flash('New category added')
            return redirect(url_for('defaultgearcategories'))
        else: # Handle GET requests
            form = AddCategoryForm()
            return render_template('add_category.html', 
				   form=form,
                                   login_session=login_session,
				   CLIENT_ID=CLIENT_ID, )


@app.route('/delete_category/<int:category_id>/', methods=['GET', 'POST'])
def deletegearcategory(category_id):
    """For a given category_id delete the models and category related to the category_id"""

    # Verify user is logged in
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


#Individual gear model handlers
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
            form = ModelForm(request.form)
            if not form.validate():
                return render_template('model_form.html', 
				       form=form,
                                       category=category,
                                       login_session=login_session,
				       CLIENT_ID=CLIENT_ID, )

            model = GearModels()
            # Populate fields
            form.populate_obj(model)
            model.category = category
            model.user_id = login_session['name']
            session.add(model)

            # Store model to DB
            session.commit()
            flash('New model created')

            # Retrieve image if it exists

            image = request.files['image']
            if image:

                # Check extensions to make sure image file is of correct type....

                if allowed_image(image.filename):

                    # Add image to DB

                    model.image_path = add_image(image, model.id)
                    flash('Image uploaded')
                else:

                    # Flash error if image type is incorrect

                    flash('Image not uploaded, type must be %s'
                          % list(ALLOWED_IMG_EXTENSIONS))
            else:

                # Assign a defualt image to the model if no image was provided

                model.image_path = url_for('uploaded_img',
                                           filename='image_missing.png')

            # Retrieve file if it exists

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

            form = ModelForm()
            return render_template('model_form.html', 
				   form=form,
                                   category=category,
                                   login_session=login_session,
				   CLIENT_ID=CLIENT_ID, )


@app.route('/view_items/<int:category_id>/')
def viewmodels(category_id):
    """For a given category_id render a template with all the models in the category"""

    # Query models

    models = \
        session.query(GearModels).filter_by(category_id=category_id).order_by(GearModels.manufacturer).all()

    # Query all files

    files = session.query(UploadedFiles).all()

    # Query all images

    images = session.query(Images).all()
    return render_template(
        'view_models.html',
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
            form = ModelForm(request.form)
            # Validate form data
            if not form.validate():
                return render_template('model_form.html', 
					form=form,
                                        category=model.category,
                                        login_session=login_session,
					CLIENT_ID=CLIENT_ID, )
            form.populate_obj(model)
            

            # Retrieve updated image if it exists
            image = request.files['image']
            if image:
                path = add_image(image, model.id)
                model.image_path = path

            session.add(model)
            session.commit()
            flash('Model %s edited' % model.name)
            

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

            form = ModelForm(obj=model)
            return render_template('model_form.html', 
				   form=form,
                                   model=model, 
				   category=model.category,
                                   login_session=login_session,
				   CLIENT_ID=CLIENT_ID, )


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



#File serving handler
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Given a filename return the file"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Image serving handler
@app.route('/images/<filename>')
def uploaded_img(filename):
    """Given a filename return the image"""
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)


#JSON Handler
@app.route('/json/')
def json_call():
    """Return JSON object off all category and model data"""

    models = session.query(GearModels).all()
    return jsonify(AllModels=[model.serialize for model in models])


if __name__ == '__main__':
    app.secret_key = 'SECRET_KEY'
    app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
#    app.run(host='0.0.0.0', port=8080)
