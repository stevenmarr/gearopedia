from gearopedia import db

# from sqlalchemy.orm import relationship
# from sqlalchemy import Column, ForeignKey, Integer, String

# from datadb.Model import db.Model


class GearCategories(db.Model):
    """Categery model definition"""

    __tablename__ = 'category'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(20), nullable=False)
    user_id = db.Column(String, nullable=False)

    def __repr__(self):
        return '<Category name: %r, User ID: %r>' % (self.name, self.user_id)


class GearModels(db.Model):
    """Gear Model model definition"""

    __tablename__ = 'model'

    id = db.Column(Integer, primary_key=True)
    manufacturer = db.Column(String(80), nullable=False)
    name = db.Column(String(80), nullable=False)
    description = db.Column(String(800))
    product_url = db.Column(String(2084))
    manual_url = db.Column(String(2084))
    category_id = db.Column(Integer, ForeignKey('category.id'))
    category = db.relationship(GearCategories)
    user_id = db.Column(String, nullable=False)
    image_path = db.Column(String(250))

    def __repr__(self):
        return '<Model Name: %r, User ID: %r>' % (self.name, self.user_id)

    
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



class Images(db.Model):
    """Image file model definition"""

    __tablename__ = 'image'

    id = db.Column(Integer, primary_key=True)
    file_name = db.Column(String(80), nullable=False)
    path = db.Column(String(250), nullable=False)
    model_id = db.Column(Integer, ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)


class UploadedFiles(db.Model):
    """Uploaded files model definition"""

    __tablename__ = 'file'

    id = db.Column(Integer, primary_key=True)
    file_name = db.Column(String(80), nullable=False)
    file_type = db.Column(String(80), nullable=False)
    path = db.Column(String(250), nullable=False)
    model_id = db.Column(Integer, ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)    
