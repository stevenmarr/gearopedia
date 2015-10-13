import os
import logging
import sqlalchemy

from flask import url_for
from flask import session as login_session
from werkzeug import secure_filename

from gearopedia import app, db

from models import GearCategories, GearModels, UploadedFiles, Images
# from database import db_session as session
from forms import FILE_TYPE

session = db.session

ALLOWED_IMG_EXTENSIONS = app.config['ALLOWED_IMG_EXTENSIONS']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']


def allowed_file(filename):
    """Returns filename if the filename extension is in ALLOWED_EXTENSIONS."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def add_file(upload_file, file_type, model_id, edit=None):
    """
    Adds file to database, and writes file to server.
    If the model already has a file of the same type, the old file
    is deleted in the database and from the server and the new file
    is written.

    Keyword arguments
    edit -- a flag indicated the function was called from and edit
            operation
    """

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
                               model_id=model_id,
                               user_id=login_session['name'],
                               path=path)
    session.add(model_file)
    session.commit()
    return path


def delete_file(id):
    """Delete the file from the database and server.

    Keyword arguments
    id --- database id of the uploaded file
    """
    uploaded_file = session.query(UploadedFiles).filter_by(id=id).one()
    session.delete(uploaded_file)
    session.commit()
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.file_name))
    except OSError:
        logging.error("File does not exist")


def delete_files(model_id):
    """Delete all files associated with model.

    Keyword arguments
    model_id --- database id of the model to delete files from
    """

    files = session.query(UploadedFiles).filter_by(model_id=model_id)
    # delete files if they exist
    if files:
        map(delete_file, [f.id for f in files])


def allowed_image(filename):
    """Returns filename if the filename extension is in ALLOWED_IMG_EXTENSIONS."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS


def add_image(upload_image, model_id):
    """Upload image file and tag the image to the model.

    Keyword arguments
    upload_image --- image file to upload
    model_id -- database id of the model"""

    # Erase existing upload_image if it exists
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
    """Erase images file for model.

    Keyword arguments
    model_id ---  database id of the model"""
    try:
        image = session.query(Images).filter_by(model_id=model_id).one()
        # delete image
        if image:
            try:
                os.remove(os.path.join(app.config['UPLOAD_IMG_FOLDER'], image.file_name))
            except OSError:
                logging.info("File did not exist")
            session.delete(image)
            session.commit()
    except sqlalchemy.orm.exc.NoResultFound:
        logging.info("No images exist")


def check_login():
    """Return user name if user is logged in"""
    if 'name' not in login_session:
        raise TypeError
    else:
        return login_session['name']
