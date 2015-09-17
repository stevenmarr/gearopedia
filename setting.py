#!/usr/bin/python
import json


#APPLICATION ********************
APPLICATION_NAME = 'Gear Wiki'
#CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
#SECRET_KEY = json.loads(open('secrets.json', 'r').read())['app']['secret_key']
CLIENT_ID = json.loads(open('/var/www/gearopedia/gearopedia/client_secrets.json', 'r').read())['web']['client_id']
SECRET_KEY = json.loads(open('/var/www/gearopedia/gearopedia/secrets.json', 'r').read())['app']['secret_key']

#DATA BASE ************************
#path for database
#for local production, comment for server
#DATA_BASE = 'sqlite:///gear_wiki.db'
#for server, comment for local production
DB_PASS = json.loads(open('/var/www/gearopedia/gearopedia/secrets.json', 'r').read())['app']['database_pass']
DATA_BASE = 'postgresql://postgres:%s@localhost/gearopedia' % DB_PASS


#FILES ***************************
#folder paths
#UPLOAD_FOLDER = './files/uploads'
#UPLOAD_IMG_FOLDER = './files/img'
UPLOAD_FOLDER = '/var/www/gearopedia/files/uploads'
UPLOAD_IMG_FOLDER = '/var/www/gearopedia/files/img'
#permitted image and file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
#file types available for selection from model forms, required server restart
FILE_TYPE = {
	'0': '-',
    '1': 'Owners Manual',
    '2': 'Service Manual',
    '3': 'Firmware',
    '4': 'Software',
    '5': 'Other',
    }




