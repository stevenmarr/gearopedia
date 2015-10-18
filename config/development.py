import os

DEBUG = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gearopedia.db')
