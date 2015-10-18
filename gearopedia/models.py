from gearopedia import db

# from sqlalchemy.orm import db.relationship
# from sqlalchemy import db.Column, db.ForeignKey, db.Integer, db.String

# from datadb.Model import db.Model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class GearCategories(db.Model):
    """Categery model definition"""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Category name: %r, User ID: %r>' % (self.name, self.user_id)


class GearModels(db.Model):
    """Gear Model model definition"""

    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(800))
    product_url = db.Column(db.String(2084))
    manual_url = db.Column(db.String(2084))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(GearCategories)
    user_id = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String(250))

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

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(250), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)


class UploadedFiles(db.Model):
    """Uploaded files model definition"""

    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    file_type = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(250), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    model = db.relationship(GearModels)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<File name: %r, User ID: %r>' % (self.file_name, self.user_id)    
