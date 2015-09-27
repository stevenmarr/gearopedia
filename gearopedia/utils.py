#!/gearopedia/utils.py
import os
import logging

from flask import url_for
from flask import session as login_session
from werkzeug import secure_filename

from gearopedia import app
from models import GearCategories, GearModels, UploadedFiles, Images
from database import db_session as session

ALLOWED_IMG_EXTENSIONS = app.config['ALLOWED_IMG_EXTENSIONS']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
FILE_TYPE = app.config['FILE_TYPE']
# file helper functions
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

    # check filename extension and make secure
    if not allowed_file(upload_file.filename):
        raise TypeError
    filename = secure_filename(upload_file.filename)
    if not filename:
        raise TypeError

    # Save file
    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create new UploadedFiles object
    path = url_for('uploaded_file', filename=filename)
    model_file = UploadedFiles(file_name=filename,
                               	file_type=FILE_TYPE[file_type],
				model_id = model_id,
    				user_id = login_session['name'],
    				path = path)
    session.add(model_file)
    session.commit()
    return path


def delete_file(id):
    """For a given file id delete the file"""
    uploaded_file = session.query(UploadedFiles).filter_by(id=id).one()
    session.delete(uploaded_file)
    session.commit()
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.file_name))
    except:
        logging.error("File does not exist")


def delete_files(model_id):
    """for a given model_id, delete all its files"""
    try:
        files = session.query(UploadedFiles).filter_by(model_id=model_id)
        # delete files if they exist
        if files:
            map(delete_file, [f.id for f in files])
    except:
        logging.info("No files exist for deletion")


# image helper functions
def allowed_image(filename):
    """Return filename if extension is in ALLOWED_IMG_EXTENSIONS"""

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS


def add_image(upload_image, model_id):
    """Given an upload_image and model_id, assign the upload_image to the model"""
    # Erase existing upload_image if it exists
    model = session.query(GearModels).filter_by(id=model_id)
    delete_image(model_id)
    # check filename extension and make secure
    if not allowed_image(upload_image.filename):
        raise TypeError
    filename = secure_filename(upload_image.filename)
    if not filename:
        raise TypeError

    # Save file
    upload_image.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
    path = url_for('uploaded_img', filename=filename)
    # create new image
    image = Images(file_name=filename,
                   model_id=model_id,
                   user_id=login_session['name'],
                   path=path)
    session.add(image)
    session.commit()
    return path


def delete_image(model_id):
    """Given a model_id erase the stored image"""
    try:
        image = session.query(Images).filter_by(model_id=model_id).one()
        # delete image
        if image:
            try:
                os.remove(os.path.join(app.config['UPLOAD_IMG_FOLDER'], image.file_name))
            except:
                logging.info("File did not exist")
            session.delete(image)
            session.commit()
    except:
        logging.info("No images exist")


# login check
def check_login():
    """check for valid login"""
    if 'name' not in login_session:
        raise TypeError
    else:
        return login_session['name']