#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class GearCategories(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)


class GearModels(Base):

    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    manufacturer = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(String(800))
    product_url = Column(String(80))
    manual_url = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(GearCategories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)
    image_path = Column(String(250))

    # manual = Column(LargeBinary, nullable=True)

    @property
    def serialize(self):
        return {
            'manufacturer': self.manufacturer,
            'name': self.name,
            'description': self.description,
            'website': self.product_url,
            'category': self.category.name,
            }


class Images(Base):

    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(80), nullable=False)
    path = Column(String(250), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship(GearModels)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)


class UploadedFiles(Base):

    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(80), nullable=False)
    file_type = Column(String(80), nullable=False)
    path = Column(String(250), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship(GearModels)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)


#engine = create_engine('sqlite:///gear_wiki.db')
engine = create_engine('postgresql://postgres:marr@localhost/gearopedia')
Base.metadata.create_all(engine)
