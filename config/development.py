import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(BASE_DIR, 'gearopedia.db')
