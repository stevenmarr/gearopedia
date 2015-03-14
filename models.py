import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class GearCategories(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class GearModels(Base):
    __tablename__ = 'model'
    
    id = Column(Integer, primary_key = True)
    manufacturer = Column(String(80), nullable = False)
    model =Column(String(80), nullable = False)
    description = Column(String(250))
    product_url = Column(String(80))
    manual_url = Column(String(80))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(GearCategories) 


engine = create_engine('sqlite:///gear_wiki.db')
 

Base.metadata.create_all(engine)