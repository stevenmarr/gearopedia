# gearopedia/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from gearopedia import app
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True, pool_size=20, max_overflow=100)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    "Load models and initialize database."""

    import models
    Base.metadata.create_all(bind=engine)
