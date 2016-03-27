#!venv/bin/python

from migrate.versioning import api
from gearopedia import app, db
from gearopedia.models import GearCategories
import os.path


db.create_all()

SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = app.config['SQLALCHEMY_MIGRATE_REPO']




if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

categories = ["Video-Projectors", "Video-Switchers", "Video-Processors",
                "Video-Screens", "Audio-Console", "Audio-Microphones"]

for category in categories:
    db.session.add(GearCategories(name='%s'% category,
                                user_id="Default"))
db.session.commit()