#!/usr/bin/python
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APPLICATION_NAME = 'Gearopedia'
DEBUG = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(BASE_DIR, 'gearopedia.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
CLIENT_ID = \
    '522438111583-kpb1j28juerv3haeaak2qpq8qshetjtv.apps.googleusercontent.com'

UPLOAD_FOLDER = '%s/files/uploads' % BASE_DIR
UPLOAD_IMG_FOLDER = '%s/files/img' % BASE_DIR
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
