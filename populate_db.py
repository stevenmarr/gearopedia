from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
 
from models import GearCategories, GearModels, Base
from setting import DATA_BASE 
engine = create_engine(DATA_BASE)
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

categories = session.query(GearCategories).filter_by().all()
for category in categories:
	session.delete(category)
	session.commit()

models = session.query(GearModels).filter_by().all()
for model in models:
	session.delete(model)
	session.commit()

#Category for DLP Projectors
category1 = GearCategories(name = "Projectors")
session.add(category1)
session.commit()

category2 = GearCategories(name = "Cameras")
session.add(category2)
session.commit()

model1 = GearModels(	manufacturer = "Christie Digital",
						name = "HD14K-M", 
						description = "Christie Roadster HD14K-M 1080 HD DLP projector",
					 	product_url = "http://www.christiedigital.com/en-us/business/products/projectors/3-chip-dlp/m-series/pages/roadster-hd14k-m-3-chip-dlp-projector.aspx",
					 	manual_url = "http://www.christiedigital.com/SupportDocs/Anonymous/020-100009-08_LIT-MAN-USR-M-Series.pdf",
					 	category = category1)
						
session.add(model1)
session.commit()

model2 = GearModels(	manufacturer = "Christie Digital",
						name = "HD10K-M", 
						description = "Christie Roadster HD10K-M 1080 HD DLP projector",
					 	product_url = "http://www.christiedigital.com/en-us/business/products/projectors/3-chip-dlp/m-series/pages/roadster-hd14k-m-3-chip-dlp-projector.aspx",
					 	manual_url = "http://www.christiedigital.com/SupportDocs/Anonymous/020-100009-08_LIT-MAN-USR-M-Series.pdf",
					 	category = category1)
						
session.add(model2)
session.commit()

model2 = GearModels(	manufacturer = "Sony",
						name = "HXC100", 
						description = "Three 2/3-inch Power HAD FX CCD sensors compact portable SD / HD camera",
					 	product_url = "http://www.pro.sony.eu/pro/lang/en/eu/product/broadcast-products-system-cameras-hd-system-cameras/hxc-100/overview/",
					 	manual_url = "http://www.pro.sony.eu/pro/lang/en/eu/support/operation-manual/1237485705077",
					 	category = category2)
						
session.add(model2)
session.commit()