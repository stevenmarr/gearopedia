DEBUG = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(BASE_DIR, 'gearopedia.db')
