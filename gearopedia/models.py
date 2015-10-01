#!/usr/bin/python

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

from database import Base


class GearCategories(Base):
    """Categery model definition"""

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    user_id = Column(String, nullable=False)


class GearModels(Base):
    """Gear Model model definition"""

    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    manufacturer = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(String(800))
    product_url = Column(String(80))
    manual_url = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(GearCategories)
    user_id = Column(String, nullable=False)
    image_path = Column(String(250))

    @property
    def serialize(self):
        """Serialize gear models for JSON export"""

        return {'manufacturer': self.manufacturer,
                'name': self.name,
                'description': self.description,
                'website': self.product_url,
                'category': self.category.name,
                'user_id': self.user_id
                }


class Images(Base):
    """Image file model definition"""

    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(80), nullable=False)
    path = Column(String(250), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship(GearModels)
    user_id = Column(String, nullable=False)


class UploadedFiles(Base):
    """Uploaded files model definition"""

    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(80), nullable=False)
    file_type = Column(String(80), nullable=False)
    path = Column(String(250), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship(GearModels)
    user_id = Column(String, nullable=False)

