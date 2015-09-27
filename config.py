#!/usr/bin/python
#config.py
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APPLICATION_NAME = 'Gearopedia'
DEBUG = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI= \
'sqlite:///gear_wiki.db'
CLIENT_ID= \
'522438111583-kpb1j28juerv3haeaak2qpq8qshetjtv.apps.googleusercontent.com'

UPLOAD_FOLDER = '%s/files/uploads' % BASE_DIR
UPLOAD_IMG_FOLDER = '%s/files/img' % BASE_DIR
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_TYPE = {
    '0': '-',
    '1': 'Owners Manual',
    '2': 'Service Manual',
    '3': 'Firmware',
    '4': 'Software',
    '5': 'Other',
}
# APPLICATION ********************

# uncomment for development server
#CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
#SECRET_KEY = json.loads(open('secrets.json', 'r').read())['app']['secret_key']
# uncomment for production server
# CLIENT_ID = json.loads(open('/var/www/gearopedia/gearopedia/client_secrets.json', 'r').read())['web']['client_id']
# SECRET_KEY = json.loads(open('/var/www/gearopedia/gearopedia/secrets.json', 'r').read())['app']['secret_key']

# DATA BASE ************************
# uncomment for development server
#DATA_BASE = 'sqlite:///gear_wiki.db'
# uncomment for production server
# DB_PASS = json.loads(open('/var/www/gearopedia/gearopedia/secrets.json', 'r').read())['app']['database_pass']
# DATA_BASE = 'postgresql://postgres:%s@localhost/gearopedia' % DB_PASS


# FILES ***************************
# uncomment for development server
#UPLOAD_FOLDER = '/vagrant/catalog/files/uploads'
#UPLOAD_IMG_FOLDER = '/vagrant/catalog/files/img'
# uncomment for production server
# UPLOAD_FOLDER = '/var/www/gearopedia/files/uploads'
# UPLOAD_IMG_FOLDER = '/var/www/gearopedia/files/img'


# permitted image and file extensions
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
#ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# file types available for selection from model forms, required server restart
#FILE_TYPE = {
#    '0': '-',
#   '1': 'Owners Manual',
#    '2': 'Service Manual',
#    '3': 'Firmware',
#    '4': 'Software',
#    '5': 'Other',
#}