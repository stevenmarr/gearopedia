from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import GearCategories, GearModels, Base
 
engine = create_engine('sqlite:///gear_wiki.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Category for DLP Projectors
category1 = GearCategories(name = "Projectors")

session.add(category1)
session.commit()

model1 = GearModels(	manufacturer = "Christie Digital",
						model = "HD14K-M", 
						description = "Christie Roadster HD14K-M 1080 HD DLP projector",
					 	product_url = "http://www.christiedigital.com/en-us/business/products/projectors/3-chip-dlp/m-series/pages/roadster-hd14k-m-3-chip-dlp-projector.aspx",
					 	manual_url = "http://www.christiedigital.com/SupportDocs/Anonymous/020-100009-08_LIT-MAN-USR-M-Series.pdf",
					 	category = category1)
						
session.add(model1)
session.commit()