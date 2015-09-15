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

from models import GearCategories, GearModels, Base, Users, UploadedFiles, Images

from setting import FILE_TYPE

from forms import AddCategoryForm, ModelForm

import random
import string
import httplib2
import json
import requests
import os

    
app = Flask(__name__)

engine = create_engine('postgresql://postgres:d@+@@localhost/gearwiki')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('/var/www/gear-wiki/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Gear Wiki'

UPLOAD_FOLDER = '/home/vagrant/files/uploads'
UPLOAD_IMG_FOLDER = '/home/vagrant/files/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER


@app.route('/')
def defaultgearcategories():
    """Render home page"""

    categories = session.query(GearCategories).all()
    return render_template('default.html', categories=categories,
                           login_session=login_session,
                           page_title='Categories')


def allowed_file(filename):
    """Return filename if extension is in ALLOWED_EXTENSIONS"""

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_image(filename):
    """Return filename if extension is in ALLOWED_IMG_EXTENSIONS"""

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS


def createuser(login):
    """Create new user, return the user_id"""

    newuser = Users(name=login['username'],
                    email=login['email'],
                    picture=login['picture'])
    session.add(newuser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getuserid(email):
    """For an email address return the user_id"""
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
       return None

def getuserinfo(user_id):
    """For a user_id return the user"""

    user = session.query(Users).filer_by(id=user_id).one()
    return user


@app.route('/login', methods=['GET'])
def showlogin():
    """Login user"""
    #logging.info('Decorator ran')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    print "hello"
	#return render_template('main.html')
    return render_template('login.html', STATE=state,
                           login_session=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Run google oauth2 workflow"""

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('/var/www/gear-wiki/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps(
                'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps(
                "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.


    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 300px; height: 300px;border-radius:\
         150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    user_id = getuserid(login_session['email'])
    if not user_id:
        user_id = createuser(login_session)
    login_session['user_id'] = user_id
    flash('you are now logged in as %s' % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnect current user"""

    # Only disconnect a connected user

    credentials = login_session.get('credentials')
    if credentials is None:
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['credentials']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the users session

        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('You are now logged out.')
        return redirect('/')
    else:

        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # if for some reason the token was invalid

        response = \
            make_response(json.dumps('Failed to revoke token for given user.'
                                     , 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/add_category/', methods=['GET', 'POST'])
def addgearcategory():
    """Handler for adding a new gear category"""

    # Verify user is logged in

    if 'username' not in login_session:
        return redirect('/login')

    # Handle POST requests

    if request.method == 'POST':
        form = AddCategoryForm(request.form)

        # Validate form data

        if not form.validate():
            # render form with errors

            return render_template('add_category.html', form=form)

        # Store new category in db

        new_category = GearCategories(name=form.name.data,
                                      user_id=login_session['user_id'])
        session.add(new_category)
        session.commit()
        flash('New category added')
        return redirect(url_for('defaultgearcategories'))
    else:

        # Handle GET requests

        form = AddCategoryForm()
        return render_template('add_category.html', form=form,
                               login_session=login_session)


@app.route('/delete_category/<int:category_id>/', methods=['GET', 'POST'
                                                           ])
def deletegearcategory(category_id):
    """For a given category_id delete the models and category related to the category_id"""

    # Verify user is logged in

    if 'username' not in login_session:
        return redirect('/login')
    category = \
        session.query(GearCategories).filter_by(id=category_id).one()

    # Handle POST requests

    if request.method == 'POST':
        models = \
            session.query(GearModels).filter_by(category=category).all()

        # Deleting a category also deletes the models in the category

        for model in models:
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
                               login_session=login_session)


@app.route('/view_items/<int:category_id>/')
def viewmodels(category_id):
    """For a given category_id render a template with all the models in the category"""

    # Query models

    models = \
        session.query(GearModels).filter_by(category_id=category_id).all()

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
    )


@app.route('/add_item/<int:category_id>/', methods=['GET', 'POST'])
def addmodel(category_id):
    """For a given category_id add a model"""

    # Verify user is logged in

    if 'username' not in login_session:
        return redirect('/login')

    # Retrieve category from DB

    category = \
        session.query(GearCategories).filter_by(id=category_id).one()

    # Handle POST requests

    if request.method == 'POST':

        # Render form

        form = ModelForm(request.form)

        # Validate form data

        if not form.validate():
            # Render form with errors

            return render_template('model_form.html', form=form,
                                   category=category,
                                   login_session=login_session)

        # Create a new GearModels object

        model = GearModels()

        # Populate fields

        form.populate_obj(model)
        model.category = category
        model.user_id = login_session['user_id']
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
	        add_file(model_file, form.file_type.data, model.id)
	        flash('File upload successful')
	    except TypeError:
		flash('File type incorrect')
	    except OSError:
		flash('File upload error')
	    

            # Check extensions to make sure file is of correct type

           # if allowed_file(model_file.filename):

                # Add file to DB

            #    if add_file(model_file, form.file_type.data, model.id):
             #       flash('File upload successful.')
           # else:

                # Flash error if image type is incorrect

            #    flash('File type incorrect must be of type %s'
             #         % list(ALLOWED_EXTENSIONS))

        return redirect(url_for('viewmodels',
                                category_id=model.category_id))
    else:

        # Handle GET requests

        form = ModelForm()
        return render_template('model_form.html', form=form,
                               category=category,
                               login_session=login_session)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Given a filename return the file"""

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/images/<filename>')
def uploaded_img(filename):
    """Given a filename return the image"""

    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)


@app.route('/edit_model/<int:model_id>/', methods=['GET', 'POST'])
def editmodel(model_id):
    """Render the model_form page with model to update"""

    # Verify user is logged in

    if 'username' not in login_session:
        return redirect('/login')

    # Query for model
    
    model = session.query(GearModels).filter_by(id=model_id).one()

    # Handle POST reuests

    if request.method == 'POST':
        form = ModelForm(request.form)

        # Validate form data

        if not form.validate():
            # Render form with erros

            return render_template('model_form.html', form=form,
                                   category=model.category,
                                   login_session=login_session)

        # Populate fields

        form.populate_obj(model)
        session.add(model)

        # Store model to DB

        session.commit()
        flash('Model %s edited' % model.name)
        image = request.files['image']

        # Retrieve updated image if it exists

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

        # Retrieve updated file if it exists

        model_file = request.files['file']
        if model_file:
            flash ("sent file_type %s" % form.file_type.data)
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

        # Handle POST requests

        form = ModelForm(obj=model)
        return render_template('model_form.html', form=form,
                               model=model, category=model.category,
                               login_session=login_session)


@app.route('/delete_model/<int:model_id>/', methods=['GET', 'POST'])
def deletemodel(model_id):
    """For a given model_id delete the model"""

    # Verify user is logged in

    if 'username' not in login_session:
        return redirect('/login')

    # Query for model

    model = session.query(GearModels).filter_by(id=model_id).one()

    # Handle POST requests

    if request.method == 'POST':

        # Delete file/image entries for model
	files = session.query(UploadedFiles).filter_by(model_id=model_id).all()
        map(delete_file, [f.id for f in files])
	images = session.query(Images).filter_by(model_id=model_id).all()
	for i in images:
	    session.delete(i)
	    session.commit()

        # Delete model from DB
               
        session.delete(model)
        session.commit()
        flash('Model %s deleted' % model.name)
        return redirect(url_for('viewmodels',
                                category_id=model.category_id))
    else:

        # Handle GET requests

        return render_template('delete_model.html', model=model,
                               login_session=login_session)


@app.route('/json/')
def json_call():
    """Return JSON object off all category and model data"""

    models = session.query(GearModels).all()
    return jsonify(AllModels=[model.serialize for model in models])


def add_image(image, model_id):
    """take in image and model_id image is related to, return path to image"""

    try:

        # Create a secure filename

        filename = secure_filename(image.filename)

        # Create new Images object

        new_image = Images()

        # Assign file name

        new_image.file_name = filename

        # Create path

        path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)

        # Save image

        image.save(path)

        # Populate Images fields

        new_image.model_id = model_id
        new_image.user_id = login_session['user_id']
        new_image.path = url_for('path', filename=filename)

        # Add to DB

        session.add(new_image)
        session.commit()
        return new_image.path
    except:
        # Return path of default image
	return None
        #return url_for('uploaded_img', filename='image_missing.png')


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
    uploaded_file = session.query(UploadedFiles).filter_by(id=id).one()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.file_name))
    session.delete(uploaded_file)
    session.commit()    
	
if __name__ == '__main__':
    app.run(use_debugger=True, debug=app.debug,
            use_reloader=True)
