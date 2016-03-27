import os
import logging
import sqlalchemy

from flask import render_template, url_for, request, redirect, flash, jsonify, Blueprint
from flask import session as login_session
from flask import send_from_directory
from oauth2client import client, crypt

from ..models import GearCategories, GearModels, UploadedFiles, Images
from ..forms import AddCategoryForm, ModelForm, LoginForm
from gearopedia import app, db
# import db.db_session as session
from ..utils import login_required


session = db.session

CLIENT_ID = app.config['CLIENT_ID']


categories_blueprint=Blueprint(
    'categories', __name__,
    template_folder='templates')


# Category Handlers
@categories_blueprint.route('/add_category/', methods=['GET', 'POST'])
@login_required
def addgearcategory():
    """Create a new gear category."""
    #if check_login():
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
        return redirect(url_for('home.default'))
    else:  # Handle GET requests
        form = AddCategoryForm()
        return render_template('add_category.html',
                               form=form,
                               login_session=login_session,
                               CLIENT_ID=CLIENT_ID)


@categories_blueprint.route('/delete_category/<int:category_id>/', methods=['GET', 'POST'])
@login_required
def deletegearcategory(category_id):
    """Delete a gear category."""
    try:
        category = \
            session.query(GearCategories).filter_by(id=category_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
         flash('Error deleting')
         return redirect(url_for('default'))
    if request.method == 'POST':
        category.delete_category()
        flash('Category %s deleted' % category.name)
        return redirect(url_for('home.default'))
    else:
        return render_template('delete_category.html',
                               category=category,
                               login_session=login_session,
                               CLIENT_ID=CLIENT_ID, )
