#!/Users/personal/gearopedia/venv/bin/python
import os
import unittest

from gearopedia import app, db

from gearopedia.models import GearModels

BASE_DIR = app.config['BASE_DIR']

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        
        self.app = app.test_client()
        db.create_all()
        
    def teadDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_gear_model(self):
        u = GearModels(manufacturer="Test Manu",
                        name="Test Name",
                        description="Test Desc",
                        product_url="http://www.example.com",
                        user_id="Unit Test")
        
if __name__ == '__main__':
    unittest.main()
