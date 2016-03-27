import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
        
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APPLICATION_NAME = 'Gearopedia'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
    CLIENT_ID = \
        '522438111583-kpb1j28juerv3haeaak2qpq8qshetjtv.apps.googleusercontent.com'
    UPLOAD_FOLDER = '%s/files/uploads' % BASE_DIR
    UPLOAD_IMG_FOLDER = '%s/files/img' % BASE_DIR
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg'}
    ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    ADMINS = []
    MAIL_SERVER = ''
    MAIL_PORT  = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI= \
        'postgresql://postgres:%s@localhost/gearopedia' % 'cheese'
