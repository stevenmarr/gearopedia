import os
import logging

from gearopedia import db, app
from forms import FILE_TYPE

from flask import url_for, flash, redirect
from flask import session as login_session

from werkzeug import secure_filename
# from sqlalchemy.orm import db.relationship
# from sqlalchemy import db.Column, db.ForeignKey, db.Integer, db.String

# from datadb.Model import db.Model
ALLOWED_IMG_EXTENSIONS = app.config['ALLOWED_IMG_EXTENSIONS']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class GearCategories(db.Model):
    """Categery model definition"""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Category name: %r, User ID: %r>' % (self.name, self.user_id)


class GearModels(db.Model):
    """Gear Model model definition"""

    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(800))
    product_url = db.Column(db.String(2084))
    manual_url = db.Column(db.String(2084))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(GearCategories)
    user_id = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String(250))

    def __repr__(self):
        return '<Model Name: %r, User ID: %r>' % (self.name, self.user_id)

    
    @property
    def serialize(self):
        """Serialize gear models for JSON export"""

        return {'manufacturer': self.manufacturer,
                'name': self.name,
                'description': self.description,
                'website': self.product_url,
                'category': self.category.name,
                'user_id': self.user_id
                }
    def delete(self):
        UploadedFiles.delete_files(self.id)
        Images.delete_image(self.id)
        db.session.delete(self)
        db.session.commit()
        #TODO delete_files(model_id)
        #TODO delete_image(model_id)


class Images(db.Model):
    """Image file model definition"""
    #TODO Refactor so images are just another file
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(250), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)

    @staticmethod
    def allowed_image(filename):
        """Returns filename if the filename extension is in ALLOWED_IMG_EXTENSIONS."""
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS

    @classmethod
    def add_image(cls, upload_image, model_id):
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
        image = cls(file_name=filename,
                       model_id=model_id,
                       user_id=login_session['name'],
                       path=path)
        db.session.add(image)
        db.session.commit()
        return path

    @classmethod
    def delete_image(cls, model_id):
        """Erase images file for model.

        Keyword arguments
        model_id ---  database id of the model"""
        try:
            image = db.session.query(cls).filter_by(model_id=model_id).one()
            # delete image
            if image:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_IMG_FOLDER'], image.file_name))
                except OSError:
                    logging.info("File did not exist")
                session.delete(image)
                session.commit()
        except:
            logging.info("No images exist")



class UploadedFiles(db.Model):
    """Uploaded files model definition"""

    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    file_type = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(250), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)   

    @classmethod
    def allowed_image(cls, filename):
        """Returns filename if the filename extension is in ALLOWED_IMG_EXTENSIONS."""
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS

    @staticmethod
    def allowed_file(filename):
        """Returns filename if the filename extension is in ALLOWED_EXTENSIONS."""
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @classmethod
    def add_file(cls, upload_file, file_type, model_id, edit=None):
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
                db.session.query(cls).filter_by(model_id=model_id)
            map(cls.delete_file, [model_file.id for model_file in model_files if model_file.file_type == FILE_TYPE[file_type]])

        # check filename extension and make secure
        if not cls.allowed_file(upload_file.filename):
            raise TypeError
        filename = secure_filename(upload_file.filename)
        if not filename:
            raise TypeError

        # Save file
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create new UploadedFiles object
        path = url_for('uploaded_file', filename=filename)
        model_file = cls(file_name=filename,
                                   file_type=FILE_TYPE[file_type],
                                   model_id=model_id,
                                   user_id=login_session['name'],
                                   path=path)
        db.session.add(model_file)
        db.session.commit()
        return path


    @classmethod
    def delete_file(cls, id):
        """Delete the file from the database and server.

        Keyword arguments
        id --- database id of the uploaded file
        """
        uploaded_file = db.session.query(cls).filter_by(id=id).one()
        db.session.delete(uploaded_file)
        db.session.commit()
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.file_name))
        except OSError:
            logging.error("File does not exist")            

    @classmethod
    def delete_files(cls, model_id):
        """Delete all files associated with model.

        Keyword arguments
        model_id --- database id of the model to delete files from
        """

        files = db.session.query(cls).filter_by(model_id=model_id)
        # delete files if they exist
        if files:
            map(cls.delete_file, [f.id for f in files])






















