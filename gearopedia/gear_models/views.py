import sqlalchemy
from flask import render_template, url_for, request, redirect, flash, jsonify, Blueprint
from flask import session as login_session

from ..models import GearCategories, GearModels, UploadedFiles, Images
from ..forms import ModelForm
from gearopedia import app, db
# import db.db_session as session
from ..utils import login_required


session = db.session

CLIENT_ID = app.config['CLIENT_ID']

gear_models_blueprint = Blueprint(
    'gearModels', __name__,
    template_folder='templates')


# Individual gear model handlers


@gear_models_blueprint.route('/add_item/<int:category_id>/', methods=['GET', 'POST'])
@login_required
def addmodel(category_id):
    """Create a new gear model."""
# Retrieve category from DB
    category = \
        session.query(GearCategories).filter_by(id=category_id).one()
    # Handle POST requests
    if request.method == 'POST':
        # Render form, validate data
        form = ModelForm(request.form)
        if not form.validate():
            flash('There was an error on the form %s.' % form.errors)
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
            model.image_path = Images.add_image(image, model.id)
        session.add(model)
        session.commit()
        flash('New model created, File Type is %s' % form.file_type.data)
        
        # check for file upload if one exists
        uploaded_file = request.files['file']
        
        if uploaded_file:
            try:
                UploadedFiles.add_file(uploaded_file, form.file_type.data, model.id, edit=True)
                flash('File upload successful')
            except TypeError:
                flash('File type incorrect')
            except OSError:
                flash('File upload error')
        print "redirect model.category_id = %s" % model.category_id
        return redirect(url_for('gearModels.viewmodels',
                                category_id=model.category_id))
    else:
        # Handle GET requests
        form = ModelForm()
        return render_template('model_form.html',
                               form=form,
                               category=category,
                               login_session=login_session,
                               CLIENT_ID=CLIENT_ID)


@gear_models_blueprint.route('/view_items/<int:category_id>/')
def viewmodels(category_id):
    """View all models for a given category."""
    try:    
        models = \
            session.query(GearModels).filter_by(category_id=category_id).order_by(GearModels.manufacturer).all()
    except sqlalchemy.orm.exc.NoResultFound:
        flash('Page not found')
        return redirect(url_for('default'))
    
    try:
        category = \
            session.query(GearCategories).filter_by(id=category_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        flash('Page not found')
        return redirect(url_for('default'))
    files = session.query(UploadedFiles).all()
    images = session.query(Images).all()
    return render_template('view_models.html',
                           title="Models",
                           models=models,
                           category_id=category_id,
                           category=category,
                           login_session=login_session,
                           files=files,
                           images=images,
                           CLIENT_ID=CLIENT_ID)


@gear_models_blueprint.route('/edit_model/<int:model_id>/', methods=['GET', 'POST'])
@login_required
def editmodel(model_id):
    """Edit a gear model."""
    try:
        model = session.query(GearModels).filter_by(id=model_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        flash('Page not found')
        return redirect(url_for('default'))
    if request.method == 'POST':
        form = ModelForm(request.form, )
        # Validate form data
        if not form.validate():
            return render_template('model_form.html',
                                   title="Edit Model",
                                   form=form,
                                   model=model,
                                   category=model.category,
                                   login_session=login_session,
                                   CLIENT_ID=CLIENT_ID)
        form.populate_obj(model)
        # Retrieve updated image if it exists and upload it
        image = request.files['image']
        if image:
            model.image_path = Images.add_image(image, model.id)
# add model to db
        session.add(model)
        session.commit()
        flash('Model %s edited' % model.name)

        # check for file upload if one exists
        model_file = request.files['file']
        if model_file:
            try:
                UploadedFiles.add_file(model_file, form.file_type.data, model.id, edit=True)
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


@gear_models_blueprint.route('/delete_model/<int:model_id>/', methods=['GET', 'POST'])
@login_required
def deletemodel(model_id):
    """Delete a gear model."""

    # Verify user is logged in
    try:
        model = session.query(GearModels).filter_by(id=model_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        flash('Invalid ID')
        return redirect(url_for('default'))
    # Handle POST requests
    if request.method == 'POST':
        # Delete from DB
        # TODO add error checking
        model.delete()
        flash('Model %s deleted' % model.name)
        return redirect(url_for('viewmodels',
                                category_id=model.category_id))
    else:
        # Handle GET requests
        return render_template('delete_model.html',
                               model=model,
                               login_session=login_session,
                               CLIENT_ID=CLIENT_ID, )


# JSON Handler
@gear_models_blueprint.route('/json/')
def json_call():
    """Return JSON object off all categories and gear models."""
    models = session.query(GearModels).all()
    return jsonify(AllModels=[model.serialize for model in models])
